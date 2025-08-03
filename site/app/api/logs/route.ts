import { NextResponse } from "next/server"
import { WorkflowDatabase } from "@/lib/database"

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get("limit") || "50", 10)
    const logs = WorkflowDatabase.getRecentActivity(limit)
    return NextResponse.json(logs)
  } catch (error) {
    console.error("Failed to fetch logs:", error)
    return NextResponse.json({ error: "Failed to fetch logs" }, { status: 500 })
  }
}
