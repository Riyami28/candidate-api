from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from models import Candidate, CandidateCreate, CandidateStatusUpdate, CandidateStatus

app = FastAPI(
    title="Candidate Management API",
    description="A simple backend API to manage candidates for a recruitment system.",
    version="1.0.0",
)

# In-memory storage
candidates_db: dict[int, Candidate] = {}
next_id: int = 1


@app.post("/candidates", response_model=Candidate, status_code=201)
def create_candidate(candidate: CandidateCreate):
    """Add a new candidate to the recruitment system."""
    global next_id

    # Check for duplicate email
    for existing in candidates_db.values():
        if existing.email == candidate.email:
            raise HTTPException(
                status_code=400,
                detail=f"A candidate with email '{candidate.email}' already exists.",
            )

    new_candidate = Candidate(id=next_id, **candidate.model_dump())
    candidates_db[next_id] = new_candidate
    next_id += 1
    return new_candidate


@app.get("/candidates", response_model=list[Candidate])
def get_candidates(status: Optional[CandidateStatus] = Query(None, description="Filter candidates by status")):
    """Return all candidates, optionally filtered by status."""
    all_candidates = list(candidates_db.values())
    if status is not None:
        all_candidates = [c for c in all_candidates if c.status == status]
    return all_candidates


@app.put("/candidates/{id}/status", response_model=Candidate)
def update_candidate_status(id: int, body: CandidateStatusUpdate):
    """Update the status of a candidate by ID."""
    if id not in candidates_db:
        raise HTTPException(status_code=404, detail=f"Candidate with id {id} not found.")
    candidates_db[id].status = body.status
    return candidates_db[id]
