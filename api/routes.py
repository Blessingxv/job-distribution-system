from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

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

@router.get("/api/v1/jobs/{job_id}", response_model = JobResponse)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code = 404,
            detail = "Job Not Found"
        )

    return JobResponse(
        job_id = job.job_id,
        job_type = job.job_type,
        priority = job.priority,
        status = job.status
    )

@router.get("/api/v1/jobs/{job_id}/result", response_model = JobResponse)
def get_job_result(job_id: UUID, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)

    if not job:
        raise HTTPException(
            status_code = 404,
            detail = "Job Not Found"
        )
    elif job.status == JobStatus.PENDING.value:
        raise HTTPException(
            status_code = 409,
            detail = "Conflict: Job is still in the queue"
        )
    elif job.status == JobStatus.RUNNING.value:
        raise HTTPException(
            status_code = 409,
            detail = "Conflict: Job is still running"
        )
    elif job.status != JobStatus.COMPLETED.value:
        raise HTTPException(
            status_code = 409,
            detail = "Job Failed"
        )
    return JobResponse(
        job_id = job.job_id,
        job_type = job.job_type,
        priority = job.priority,
        status = job.status
    )
    
