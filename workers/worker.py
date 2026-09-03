import threading
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models.database import SessionLocal 
from models.job import Job
from models.enums import JobStatus
from models.executions import Execution

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_job(job_id):
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if job is None:
            raise HTTPException(
                status_code = 404,
                detail = "Job Not Found"
            )
        execution = Execution(
            execution_id = uuid.uuid4(),
            job_id = job.job_id,
            worker_id = threading.current_thread().name,
            status = JobStatus.RUNNING.value,
            started_at = lambda: datetime.now(timezone.utc),
            completed_at = None,
            error_message = None,
            error_category = None
        )
        job.status = JobStatus.RUNNING.value
        db.add(execution)
        db.commit()
    finally:
        db.close()
