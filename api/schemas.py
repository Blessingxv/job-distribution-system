from uuid import UUID
from typing import Any
from pydantic import BaseModel, Field 
from enum import Enum
from models.enums import JobStatus

class JobType(str, Enum):
    FIBONACCI = "fibonacci"
    PRIME_CHECK = "prime_check"
    BEAM_CALCULATION = "beam_calculation"

class JobCreateRequest(BaseModel):
    job_type: JobType
    payload:  dict[str, Any]
    priority: int = Field(default = 0)

class JobResponse(BaseModel): 
    job_id: UUID
    job_type: JobType
    priority: int
    status: JobStatus