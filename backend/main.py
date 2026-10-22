from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sequence import analyze_sequence

app = FastAPI(title="Genome Analysis Tool API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SequenceRequest(BaseModel):
    sequence: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: SequenceRequest):
    return analyze_sequence(request.sequence)
