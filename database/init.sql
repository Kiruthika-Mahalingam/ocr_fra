-- Create database
CREATE DATABASE fra_db;

-- Connect to the database
\c fra_db;

-- Create enum type for processing levels
CREATE TYPE processing_level AS ENUM ('level1', 'level2', 'level3', 'level4');

-- fra_records table is created by SQLAlchemy, but this is a backup SQL

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_fra_records_level ON fra_records(level);
CREATE INDEX IF NOT EXISTS idx_fra_records_status ON fra_records(status);
CREATE INDEX IF NOT EXISTS idx_fra_records_village ON fra_records(village_name);
CREATE INDEX IF NOT EXISTS idx_fra_records_district ON fra_records(district);
CREATE INDEX IF NOT EXISTS idx_fra_records_state ON fra_records(state);
CREATE INDEX IF NOT EXISTS idx_fra_records_created_at ON fra_records(created_at);