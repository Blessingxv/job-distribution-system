from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal 
from models.job import Job
from api.schemas import JobCreateRequest, JobResponse
from models.enums import JobStatus

router = APIRouter()

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/jobs", response_model = JobResponse)
def create_job(request: JobCreateRequest, db: Session = Depends(get_db)):
    new_job = Job(
        job_type = request.job_type.value,
        payload = request.payload,
        priority = request.priority,
        status = JobStatus.PENDING.value
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return JobResponse(
        job_id = new_job.job_id,
        job_type = new_job.job_type,
        priority = new_job.priority,
        status = new_job.status
    )

