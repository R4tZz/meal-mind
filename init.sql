-- Basic database setup for PostgREST
-- This creates the necessary database structure for PostgREST to work

-- Create the default schema tables if they don't exist
CREATE TABLE IF NOT EXISTS public.health_check (
    id SERIAL PRIMARY KEY,
    status TEXT DEFAULT 'healthy',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert a test record
INSERT INTO public.health_check (status) VALUES ('healthy') ON CONFLICT DO NOTHING;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;