# Supabase Local Development Setup

This directory contains the configuration and setup for the local Supabase development stack.

## Quick Start

```bash
# Start the Supabase local development environment
npx supabase start

# Stop the Supabase local development environment
npx supabase stop

# Check the status of local services
npx supabase status
```

## Services

The local Supabase stack includes the following services:

- **PostgreSQL Database** (port 54322)
- **Supabase Studio** (port 54323) - Web interface for database management
- **API Server** (port 54321) - REST and GraphQL APIs
- **Auth Server** - User authentication and authorization
- **Storage Server** - File storage with S3-compatible API
- **Realtime Server** - Real-time subscriptions
- **Inbucket** (port 54324) - Email testing interface

## Database Connection

**Connection URL:** `postgresql://postgres:postgres@127.0.0.1:54322/postgres`

**Connection Details:**
- Host: `127.0.0.1`
- Port: `54322`
- Database: `postgres`
- Username: `postgres`
- Password: `postgres`

## API Keys

When the local stack is running, you can get the current API keys with:

```bash
npx supabase status
```

The output will include:
- `anon key` - For client-side applications
- `service_role key` - For server-side applications with elevated privileges

## Storage Configuration

S3-compatible storage is available at `http://127.0.0.1:54321/storage/v1/s3`

Get the current S3 credentials with:
```bash
npx supabase status
```

## Configuration

The `config.toml` file contains all configuration settings for the local development environment. Key settings include:

- Project ID: `mealmind`
- Database port: `54322`
- API port: `54321`
- Studio port: `54323`
- Storage enabled: `true`
- Auth enabled: `true`

## Database Schema and Migrations

- Place migration files in `supabase/migrations/`
- Place seed data in `supabase/seed.sql`
- Run `npx supabase db reset` to apply migrations and seed data

## Files

- `config.toml` - Main configuration file
- `seed.sql` - Database seed data
- `.gitignore` - Ignores temporary files
- `.temp/` - Temporary files (ignored by git)

## Troubleshooting

If you encounter issues:

1. Make sure Docker is running
2. Stop and restart the stack: `npx supabase stop && npx supabase start`
3. Check logs with: `npx supabase start --debug`
4. Reset the database: `npx supabase db reset`

## Next Steps

1. Create your database schema in migration files
2. Add seed data to `seed.sql`
3. Connect your application using the connection details above
4. Use Supabase Studio to manage your database visually