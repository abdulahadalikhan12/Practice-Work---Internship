from fastapi import FastAPI

from app.routers import notes

app = FastAPI(
    title="Notes Service",
    description="A minimal FastAPI service that stores notes in a local JSON-array .txt file.",
    version="1.0.0",
)

app.include_router(notes.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "notes"}
