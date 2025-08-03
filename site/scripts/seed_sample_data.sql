-- Seed sample datasets and activity log for development or demo environments.
-- Execute after running init_database.sql if sample data is desired.

INSERT OR IGNORE INTO datasets (name, path, type, description) VALUES
('Sample Construction', '/data/construction_sample', 'yolo', 'Sample construction equipment dataset'),
('Vehicle Detection', '/data/vehicles', 'yolo', 'Vehicle detection dataset'),
('Safety Equipment', '/data/safety', 'yolo', 'Safety equipment detection dataset');

INSERT INTO activity_logs (action, details, status) VALUES
('Database initialized', '{"tables_created": 8, "indexes_created": 10}', 'success');
