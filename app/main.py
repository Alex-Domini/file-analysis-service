from fastapi import FastAPI

app = FastAPI(title="File Analysis Service")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
