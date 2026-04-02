from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class CandidateStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    selected = "selected"
    rejected = "rejected"


class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=1, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    skill: str = Field(..., min_length=1, examples=["Python"])
    status: CandidateStatus = Field(..., examples=["applied"])


class CandidateStatusUpdate(BaseModel):
    status: CandidateStatus


class Candidate(BaseModel):
    id: int
    name: str
    email: EmailStr
    skill: str
    status: CandidateStatus
