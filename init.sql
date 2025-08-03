-- Database initialization script for Collection Management System

-- Create the collections table
CREATE TABLE IF NOT EXISTS collections (
    record_id SERIAL PRIMARY KEY,
    ID INTEGER NOT NULL,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Contact VARCHAR(255),
    Date DATE DEFAULT CURRENT_DATE,
    read_only BOOLEAN DEFAULT FALSE,
    last_updated_by VARCHAR(255),
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_collections_id ON collections(ID);
CREATE INDEX IF NOT EXISTS idx_collections_read_only ON collections(read_only);
CREATE INDEX IF NOT EXISTS idx_collections_date ON collections(Date);

-- Function to prevent updates on read-only rows
CREATE OR REPLACE FUNCTION prevent_update_on_readonly()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.read_only THEN
        RAISE EXCEPTION 'This row is read-only and cannot be updated';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to update audit fields
CREATE OR REPLACE FUNCTION update_audit_fields()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    IF NEW.last_updated_by IS NULL THEN
        NEW.last_updated_by = current_user;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
DROP TRIGGER IF EXISTS check_readonly_before_update ON collections;
CREATE TRIGGER check_readonly_before_update
    BEFORE UPDATE ON collections
    FOR EACH ROW
    EXECUTE FUNCTION prevent_update_on_readonly();

DROP TRIGGER IF EXISTS update_audit_on_change ON collections;
CREATE TRIGGER update_audit_on_change
    BEFORE UPDATE ON collections
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION update_audit_fields();

-- Insert some sample data for testing
INSERT INTO collections (ID, Name, Contact, Date, read_only, last_updated_by) VALUES
(1001, 'John Doe', '0712345678', '2024-01-15', true, 'system'),
(1002, 'Jane Smith', '0723456789', '2024-01-16', false, 'system'),
(1003, NULL, '0734567890', '2024-01-17', false, 'system'),
(1001, 'John Doe Updated', '0712345678', '2024-01-18', true, 'system'); -- Multiple entries for same ID 