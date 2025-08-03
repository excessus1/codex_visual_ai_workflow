import { NextResponse } from "next/server"
import { WorkflowDatabase } from "@/lib/database"

interface ProjectPayload {
  name: string
  type: string
  status?: string
  config?: string
}

export async function GET() {
  try {
    const projects = WorkflowDatabase.getProjects()
    return NextResponse.json(projects)
  } catch (error) {
    console.error("Failed to fetch projects:", error)
    return NextResponse.json({ error: "Failed to fetch projects" }, { status: 500 })
  }
}

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as ProjectPayload

    if (!body?.name || !body?.type) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 },
      )
    }

    const id = WorkflowDatabase.createProject(body)
    const project = WorkflowDatabase.getProject(id)

    return NextResponse.json(project, { status: 201 })
  } catch (error) {
    console.error("Failed to create project:", error)
    return NextResponse.json(
      { error: "Failed to create project" },
      { status: 500 },
    )
  }
}
