from uuid import UUID
from typing import Any
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from models.enums import JobStatus
from workers.handlers import beam_calculation

class JobType(str, Enum):
    FIBONACCI = "fibonacci"
    PRIME_CHECK = "prime_check"
    BEAM_CALCULATION = "beam_calculation"

class JobCreateRequest(BaseModel):
    job_type: JobType
    payload:  dict[str, Any]
    priority: int = Field(default = 0)

    @model_validator(mode = "after")
    def validate_payload(self):
        if self.job_type == JobType.BEAM_CALCULATION:
            required = {"length", "load", "load_position", "second_moment_of_area", "extreme_fiber_distance"}
            provided = self.payload.keys()
            missing = required - provided | {key for key in required if self.payload.get(key) is None}

            if missing:
                    raise ValueError(f"Missing required fields: {missing}")
            
            if not (0 < self.payload.get("load_position") < self.payload.get("length")):
                raise ValueError("Load position must be between 0 and beam length.")
            elif self.payload.get("length") <= 0:
                raise ValueError("Beam length must be a positive value.")
            elif self.payload.get("load") <= 0:
                raise ValueError("Load must be a positive value.")
            elif self.payload.get("second_moment_of_area") <= 0:
                raise ValueError("Second moment of area must be a positive value.")
            elif self.payload.get("extreme_fiber_distance") <= 0:
                raise ValueError("Extreme fiber distance must be a positive value.")
            else:
                return self 

        if self.job_type == JobType.FIBONACCI:
            if not isinstance(self.payload.get("n"), int) or type(self.payload.get("n")) == bool:
                raise ValueError("Fibonacci job requires an integer value for 'n'.")
            elif self.payload.get("n") < 0:
                raise ValueError("Fibonacci job requires a non-negative integer value for 'n'.") 
            else:
                return self

        if self.job_type == JobType.PRIME_CHECK:
            if not isinstance(self.payload.get("n"), int) or type(self.payload.get("n")) == bool:
                raise ValueError("Prime check job requires an integer value for 'n'.")
            elif self.payload.get("n") < 2:
                raise ValueError("Prime check job requires an integer value greater than or equal to 2 for 'n'.")
            else:
                return self
            
class JobResponse(BaseModel): 
    job_id: UUID
    job_type: JobType
    priority: int
    status: JobStatus