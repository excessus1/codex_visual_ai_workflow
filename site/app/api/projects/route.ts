import { NextResponse } from "next/server"
import { WorkflowDatabase } from "@/lib/database"

export async function GET() {
  try {
    const projects = WorkflowDatabase.getProjects()
    return NextResponse.json(projects)
  } catch (error) {
    console.error("Failed to fetch projects:", error)
    return NextResponse.json({ error: "Failed to fetch projects" }, { status: 500 })
  }
}
