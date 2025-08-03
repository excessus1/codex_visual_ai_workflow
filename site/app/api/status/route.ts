import { NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"
import fs from "fs/promises"

export async function GET() {
  try {
    // Check system status
    const status = await getSystemStatus()
    return NextResponse.json(status)
  } catch (error) {
    console.error("Status check error:", error)
    return NextResponse.json({ error: "Failed to get system status" }, { status: 500 })
  }
}

async function getSystemStatus() {
  const status = {
    system: "ready",
    gpu: await getGPUStatus(),
    storage: await getStorageStatus(),
    processes: await getActiveProcesses(),
    recentLogs: await getRecentLogs(),
  }

  return status
}

async function getGPUStatus() {
  return new Promise((resolve) => {
    const process = spawn("nvidia-smi", [
      "--query-gpu=memory.used,memory.total,utilization.gpu",
      "--format=csv,noheader,nounits",
    ])
    let output = ""

    process.stdout.on("data", (data) => {
      output += data.toString()
    })

    process.on("close", (code) => {
      if (code === 0 && output.trim()) {
        const [memUsed, memTotal, utilization] = output.trim().split(", ").map(Number)
        resolve({
          available: true,
          memoryUsed: memUsed,
          memoryTotal: memTotal,
          utilization: utilization,
        })
      } else {
        resolve({ available: false })
      }
    })

    process.on("error", () => {
      resolve({ available: false })
    })
  })
}

async function getStorageStatus() {
  try {
    const stats = await fs.stat(process.cwd())
    return {
      available: true,
      // Add more storage metrics as needed
    }
  } catch {
    return { available: false }
  }
}

async function getActiveProcesses() {
  // Check for active training/prediction processes
  return []
}

async function getRecentLogs() {
  try {
    const logsDir = path.join(process.cwd(), "logs", "api")
    const files = await fs.readdir(logsDir)
    const recentFile = files.sort().pop()

    if (recentFile) {
      const content = await fs.readFile(path.join(logsDir, recentFile), "utf-8")
      return content
        .split("\n")
        .filter(Boolean)
        .slice(-10)
        .map((line) => {
          try {
            return JSON.parse(line)
          } catch {
            return { raw: line }
          }
        })
    }

    return []
  } catch {
    return []
  }
}
