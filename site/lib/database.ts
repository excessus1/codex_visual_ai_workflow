import Database from "better-sqlite3"
import path from "path"

const dataDir = process.env.DATA_DIR || path.join(process.cwd(), "data")
const dbPath = process.env.DB_PATH || path.join(dataDir, "workflow.db")
const db = new Database(dbPath)

// Initialize database schema
db.exec(`
  CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    config TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    model_name TEXT NOT NULL,
    dataset_path TEXT NOT NULL,
    epochs INTEGER,
    batch_size INTEGER,
    status TEXT DEFAULT 'pending',
    progress REAL DEFAULT 0,
    metrics TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects (id)
  );

  CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    model_name TEXT NOT NULL,
    source_path TEXT NOT NULL,
    output_path TEXT,
    confidence_threshold REAL,
    status TEXT DEFAULT 'pending',
    results_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
  );

  CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    image_count INTEGER DEFAULT 0,
    classes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    details TEXT,
    status TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX IF NOT EXISTS idx_training_status ON training_sessions(status);
  CREATE INDEX IF NOT EXISTS idx_predictions_status ON predictions(status);
  CREATE INDEX IF NOT EXISTS idx_activity_timestamp ON activity_logs(timestamp);
`)

export interface Project {
  id?: number
  name: string
  type: string
  status?: string
  config?: string
  created_at?: string
  updated_at?: string
}

export interface TrainingSession {
  id?: number
  project_id?: number
  model_name: string
  dataset_path: string
  epochs: number
  batch_size: number
  status?: string
  progress?: number
  metrics?: string
  started_at?: string
  completed_at?: string
}

export interface Prediction {
  id?: number
  project_id?: number
  model_name: string
  source_path: string
  output_path?: string
  confidence_threshold: number
  status?: string
  results_count?: number
  created_at?: string
}

export interface Dataset {
  id?: number
  name: string
  path: string
  image_count?: number
  classes?: string
  created_at?: string
}

export interface ActivityLog {
  id?: number
  action: string
  details?: string
  status?: string
  timestamp?: string
}

export class WorkflowDatabase {
  // Projects
  static createProject(project: Project): number {
    const stmt = db.prepare(`
      INSERT INTO projects (name, type, status, config)
      VALUES (?, ?, ?, ?)
    `)
    const result = stmt.run(project.name, project.type, project.status || "active", project.config)
    return result.lastInsertRowid as number
  }

  static getProjects(): Project[] {
    const stmt = db.prepare("SELECT * FROM projects ORDER BY updated_at DESC")
    return stmt.all() as Project[]
  }

  static getProject(id: number): Project | undefined {
    const stmt = db.prepare("SELECT * FROM projects WHERE id = ?")
    return stmt.get(id) as Project | undefined
  }

  static updateProject(id: number, updates: Partial<Project>): void {
    const fields = Object.keys(updates)
      .map((key) => `${key} = ?`)
      .join(", ")
    const values = Object.values(updates)
    const stmt = db.prepare(`UPDATE projects SET ${fields}, updated_at = CURRENT_TIMESTAMP WHERE id = ?`)
    stmt.run(...values, id)
  }

  // Training Sessions
  static createTrainingSession(session: TrainingSession): number {
    const stmt = db.prepare(`
      INSERT INTO training_sessions (project_id, model_name, dataset_path, epochs, batch_size, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `)
    const result = stmt.run(
      session.project_id,
      session.model_name,
      session.dataset_path,
      session.epochs,
      session.batch_size,
      session.status || "pending",
    )
    return result.lastInsertRowid as number
  }

  static getTrainingSessions(): TrainingSession[] {
    const stmt = db.prepare("SELECT * FROM training_sessions ORDER BY started_at DESC")
    return stmt.all() as TrainingSession[]
  }

  static updateTrainingSession(id: number, updates: Partial<TrainingSession>): void {
    const fields = Object.keys(updates)
      .map((key) => `${key} = ?`)
      .join(", ")
    const values = Object.values(updates)
    const stmt = db.prepare(`UPDATE training_sessions SET ${fields} WHERE id = ?`)
    stmt.run(...values, id)
  }

  // Predictions
  static createPrediction(prediction: Prediction): number {
    const stmt = db.prepare(`
      INSERT INTO predictions (project_id, model_name, source_path, output_path, confidence_threshold, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `)
    const result = stmt.run(
      prediction.project_id,
      prediction.model_name,
      prediction.source_path,
      prediction.output_path,
      prediction.confidence_threshold,
      prediction.status || "pending",
    )
    return result.lastInsertRowid as number
  }

  static getPredictions(): Prediction[] {
    const stmt = db.prepare("SELECT * FROM predictions ORDER BY created_at DESC")
    return stmt.all() as Prediction[]
  }

  static updatePrediction(id: number, updates: Partial<Prediction>): void {
    const fields = Object.keys(updates)
      .map((key) => `${key} = ?`)
      .join(", ")
    const values = Object.values(updates)
    const stmt = db.prepare(`UPDATE predictions SET ${fields} WHERE id = ?`)
    stmt.run(...values, id)
  }

  // Datasets
  static createDataset(dataset: Dataset): number {
    const stmt = db.prepare(`
      INSERT INTO datasets (name, path, image_count, classes)
      VALUES (?, ?, ?, ?)
    `)
    const result = stmt.run(dataset.name, dataset.path, dataset.image_count || 0, dataset.classes)
    return result.lastInsertRowid as number
  }

  static getDatasets(): Dataset[] {
    const stmt = db.prepare("SELECT * FROM datasets ORDER BY created_at DESC")
    return stmt.all() as Dataset[]
  }

  // Activity Logs
  static logActivity(log: ActivityLog): number {
    const stmt = db.prepare(`
      INSERT INTO activity_logs (action, details, status)
      VALUES (?, ?, ?)
    `)
    const result = stmt.run(log.action, log.details, log.status)
    return result.lastInsertRowid as number
  }

  static getRecentActivity(limit = 50): ActivityLog[] {
    const stmt = db.prepare("SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?")
    return stmt.all(limit) as ActivityLog[]
  }
}

export default db
