from fastapi import FastAPI
import os
import psycopg2

app = FastAPI(title="MealMind API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to MealMind API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/db-test")
def test_database_connection():
    """Test database connectivity"""
    try:
        database_url = os.getenv(
            "DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres"
        )

        # Parse the connection string
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return {
            "status": "success",
            "message": "Database connection successful",
            "database_version": version,
        }
    except ImportError:
        return {
            "status": "error",
            "message": "psycopg2 not installed. Install with: pip install psycopg2-binary",
        }
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}


def hello() -> str:
    return "Hello from api!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
