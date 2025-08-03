import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs/promises"
import { WorkflowDatabase } from "@/lib/database"
import { allowedScripts } from "@/config/scripts"
import { DATA_DIR } from "@/lib/paths"

export async function POST(request: NextRequest) {
  try {
    const { script, config, action } = await request.json()

    // Validate script name to prevent path traversal
    if (!allowedScripts.includes(script)) {
      return NextResponse.json({ error: "Invalid script name" }, { status: 400 })
    }

    // Create temporary config file if config is provided
    let configPath: string | null = null
    if (config) {
      const configDir = path.join(DATA_DIR, "temp", "configs")
      await fs.mkdir(configDir, { recursive: true })
      configPath = path.join(configDir, `config_${Date.now()}.json`)
      await fs.writeFile(configPath, JSON.stringify(config, null, 2))
    }

    // Prepare command arguments
    const args = configPath ? ["-m", script, configPath] : ["-m", script]

    let child
    try {
      child = spawn("python3", args)
    } catch (error) {
      console.error("Failed to spawn script:", error)
      if (configPath) {
        try {
          await fs.unlink(configPath)
        } catch {}
      }
      WorkflowDatabase.logActivity({
        action: "script_error",
        details: JSON.stringify({ error: String(error) }),
        status: "error",
      })
      return NextResponse.json(
        { error: "Failed to start script", details: String(error) },
        { status: 500 },
      )
    }

    const encoder = new TextEncoder()
    let buffer = ""

    // Insert initial database row based on action
    let recordId: number | null = null
    if (action === "train") {
      recordId = WorkflowDatabase.createTrainingSession({
        project_id: config?.project_id,
        model_name: config?.model,
        dataset_path: config?.data,
        epochs: config?.epochs,
        batch_size: config?.batch,
        status: "running",
      })
    } else if (action === "predict") {
      recordId = WorkflowDatabase.createPrediction({
        project_id: config?.project_id,
        model_name: config?.model,
        source_path: config?.source,
        output_path: config?.output,
        confidence_threshold: config?.conf,
        status: "running",
      })
    }

    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        const send = (type: string, data: any) => {
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type, data })}\n\n`),
          )
        }

        child.stdout.on("data", (chunk) => {
          const text = chunk.toString()
          send("stdout", text)
          buffer += text

          const lines = buffer.split(/\r?\n/)
          buffer = lines.pop() || ""

          for (const line of lines) {
            if (action === "train" && recordId !== null) {
              const match = line.match(/Epoch\s+(\d+)\/(\d+)/i)
              if (match) {
                const current = Number(match[1])
                const total = Number(match[2])
                const progress = (current / total) * 100
                WorkflowDatabase.updateTrainingSession(recordId, {
                  progress,
                  metrics: line.trim(),
                })
              }
            }
          }
        })

        child.stderr.on("data", (chunk) => {
          send("stderr", chunk.toString())
        })

        child.on("close", async (code) => {
          if (configPath) {
            try {
              await fs.unlink(configPath)
            } catch (error) {
              console.error("Failed to clean up config file:", error)
            }
          }

          if (action === "train" && recordId !== null) {
            WorkflowDatabase.updateTrainingSession(recordId, {
              status: code === 0 ? "completed" : "failed",
              progress: 100,
              completed_at: new Date().toISOString(),
            })
          } else if (action === "predict" && recordId !== null) {
            WorkflowDatabase.updatePrediction(recordId, {
              status: code === 0 ? "completed" : "failed",
            })
          }

          WorkflowDatabase.logActivity({
            action,
            details: JSON.stringify({ script, config }),
            status: code === 0 ? "success" : "error",
          })

          send("close", { code })
          controller.close()
        })

        child.on("error", (err) => {
          console.error("Process error:", err)
          send("error", String(err))
          controller.close()
        })
      },
    })

    return new NextResponse(stream, {
      headers: { "Content-Type": "text/event-stream" },
    })
  } catch (error) {
    console.error("Script execution error:", error)
    WorkflowDatabase.logActivity({
      action: "script_error",
      details: JSON.stringify({ error: String(error) }),
      status: "error",
    })
    return NextResponse.json(
      { error: "Script execution failed", details: String(error) },
      { status: 500 },
    )
  }
}
