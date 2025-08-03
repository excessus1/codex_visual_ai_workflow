import { NextResponse } from "next/server"
import { WorkflowDatabase } from "@/lib/database"

export async function GET() {
  try {
    const datasets = WorkflowDatabase.getDatasets()
    return NextResponse.json(datasets)
  } catch (error) {
    console.error("Failed to fetch datasets:", error)
    return NextResponse.json({ error: "Failed to fetch datasets" }, { status: 500 })
  }
}
