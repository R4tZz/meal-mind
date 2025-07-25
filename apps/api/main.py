from fastapi import FastAPI

app = FastAPI(title="MealMind API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to MealMind API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def hello() -> str:
    return "Hello from api!"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
