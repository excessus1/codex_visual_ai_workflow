import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs/promises"

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

    const scriptPath = path.join(process.cwd(), "scripts", script)

    // Create temporary config file if config is provided
    let configPath = null
    if (config) {
      const configDir = path.join(process.cwd(), "temp", "configs")
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

      process.stdout.on("data", (data) => {
        stdout += data.toString()
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

        // Log the action
        await logAction({
          action,
          script,
          config,
          exitCode: code,
          stdout,
          stderr,
          timestamp: new Date().toISOString(),
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
    return NextResponse.json({ error: "Script execution failed" }, { status: 500 })
  }
}

async function logAction(logData: any) {
  try {
    const logsDir = path.join(process.cwd(), "logs", "api")
    await fs.mkdir(logsDir, { recursive: true })

    const logFile = path.join(logsDir, `actions_${new Date().toISOString().split("T")[0]}.log`)
    const logEntry = JSON.stringify(logData) + "\n"

    await fs.appendFile(logFile, logEntry)
  } catch (error) {
    console.error("Failed to log action:", error)
  }
}
