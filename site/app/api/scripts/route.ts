import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs/promises"
import { WorkflowDatabase } from "@/lib/database"

export async function POST(request: NextRequest) {
  try {
    const { script, config, action } = await request.json()

    // Validate script name to prevent path traversal
    const allowedScripts = [
      "run_yolo.py",
      "collect_images.py",
      "convert_yolo_to_ls.py",
      "download_annotated.py",
      "generate_data_yaml.py",
      "index_predictions_by_class.py",
    ]

    if (!allowedScripts.includes(script)) {
      return NextResponse.json({ error: "Invalid script name" }, { status: 400 })
    }

    const scriptsDir = process.env.SCRIPTS_DIR || path.join(process.cwd(), "..", "initial", "scripts")
    const scriptPath = path.join(scriptsDir, script)

    // Create temporary config file if config is provided
    let configPath = null
    if (config) {
      const dataDir = process.env.DATA_DIR || path.join(process.cwd(), "..", "data")
      const configDir = path.join(dataDir, "temp", "configs")
      await fs.mkdir(configDir, { recursive: true })
      configPath = path.join(configDir, `config_${Date.now()}.json`)
      await fs.writeFile(configPath, JSON.stringify(config, null, 2))
    }

    // Prepare command arguments
    const args = configPath ? [scriptPath, configPath] : [scriptPath]

    return new Promise((resolve) => {
      const process = spawn("python3", args)
      let stdout = ""
      let stderr = ""
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

      process.stdout.on("data", (data) => {
        const text = data.toString()
        stdout += text
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

      process.stderr.on("data", (data) => {
        stderr += data.toString()
      })

      process.on("close", async (code) => {
        // Clean up temporary config file
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

        resolve(
          NextResponse.json({
            success: code === 0,
            exitCode: code,
            stdout,
            stderr,
          }),
        )
      })
    })
  } catch (error) {
    console.error("Script execution error:", error)
    WorkflowDatabase.logActivity({
      action: "script_error",
      details: JSON.stringify({ error: String(error) }),
      status: "error",
    })
    return NextResponse.json({ error: "Script execution failed" }, { status: 500 })
  }
}
