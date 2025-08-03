import { NextResponse } from "next/server"
import { WorkflowDatabase } from "@/lib/database"

export async function GET() {
  try {
    const sessions = WorkflowDatabase.getTrainingSessions()
    return NextResponse.json(sessions)
  } catch (error) {
    console.error("Failed to fetch training sessions:", error)
    return NextResponse.json(
      { error: "Failed to fetch training sessions" },
      { status: 500 },
    )
  }
}

