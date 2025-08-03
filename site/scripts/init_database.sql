-- Initialize the Visual AI Workflow database schema
-- This script sets up all necessary tables for the application

-- Projects table - stores workflow projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('training', 'prediction', 'dataset')),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived', 'failed')),
    description TEXT,
    config TEXT, -- JSON configuration
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Training sessions table
CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    dataset_path TEXT NOT NULL,
    data_yaml_path TEXT,
    epochs INTEGER DEFAULT 100,
    batch_size INTEGER DEFAULT 16,
    image_size INTEGER DEFAULT 640,
    learning_rate REAL DEFAULT 0.01,
    weight_decay REAL DEFAULT 0.0005,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    progress REAL DEFAULT 0,
    current_epoch INTEGER DEFAULT 0,
    best_map REAL,
    final_loss REAL,
    metrics TEXT, -- JSON metrics data
    output_path TEXT,
    model_path TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_path TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_type TEXT DEFAULT 'directory' CHECK (source_type IN ('directory', 'single', 'video')),
    output_path TEXT,
    confidence_threshold REAL DEFAULT 0.25,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    progress REAL DEFAULT 0,
    results_count INTEGER DEFAULT 0,
    detection_summary TEXT, -- JSON summary of detections
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Datasets table
CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    path TEXT NOT NULL,
    type TEXT DEFAULT 'yolo' CHECK (type IN ('yolo', 'coco', 'labelstudio')),
    image_count INTEGER DEFAULT 0,
    train_count INTEGER DEFAULT 0,
    val_count INTEGER DEFAULT 0,
    test_count INTEGER DEFAULT 0,
    classes TEXT, -- JSON array of class names
    class_count INTEGER DEFAULT 0,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Models table
CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT DEFAULT 'yolov8' CHECK (type IN ('yolov8', 'custom')),
    variant TEXT DEFAULT 'n' CHECK (variant IN ('n', 's', 'm', 'l', 'x')),
    path TEXT NOT NULL,
    training_session_id INTEGER,
    dataset_id INTEGER,
    classes TEXT, -- JSON array of class names
    performance_metrics TEXT, -- JSON metrics
    file_size INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (training_session_id) REFERENCES training_sessions (id),
    FOREIGN KEY (dataset_id) REFERENCES datasets (id)
);

-- Activity logs table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    entity_type TEXT, -- 'project', 'training', 'prediction', 'dataset', 'model'
    entity_id INTEGER,
    details TEXT, -- JSON details
    status TEXT CHECK (status IN ('success', 'error', 'warning', 'info')),
    user_id TEXT DEFAULT 'system',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- System metrics table
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_type TEXT NOT NULL, -- 'gpu', 'cpu', 'memory', 'disk'
    value REAL NOT NULL,
    unit TEXT,
    details TEXT, -- JSON additional details
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- File operations table
CREATE TABLE IF NOT EXISTS file_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT NOT NULL CHECK (operation_type IN ('collect', 'convert', 'transfer', 'extract')),
    source_path TEXT,
    destination_path TEXT,
    file_count INTEGER DEFAULT 0,
    bytes_processed INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    progress REAL DEFAULT 0,
    config TEXT, -- JSON configuration
    log_path TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_type ON projects(type);
CREATE INDEX IF NOT EXISTS idx_training_status ON training_sessions(status);
CREATE INDEX IF NOT EXISTS idx_training_project ON training_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_predictions_status ON predictions(status);
CREATE INDEX IF NOT EXISTS idx_predictions_project ON predictions(project_id);
CREATE INDEX IF NOT EXISTS idx_activity_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_activity_entity ON activity_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_system_metrics_type ON system_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_file_operations_status ON file_operations(status);

-- Insert default data
INSERT OR IGNORE INTO datasets (name, path, type, description) VALUES 
('Sample Construction', '/data/construction_sample', 'yolo', 'Sample construction equipment dataset'),
('Vehicle Detection', '/data/vehicles', 'yolo', 'Vehicle detection dataset'),
('Safety Equipment', '/data/safety', 'yolo', 'Safety equipment detection dataset');

-- Insert sample activity log
INSERT INTO activity_logs (action, details, status) VALUES 
('Database initialized', '{"tables_created": 8, "indexes_created": 10}', 'success');
