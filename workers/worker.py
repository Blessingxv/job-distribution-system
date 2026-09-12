import threading
import uuid
from fastapi import HTTPException
from datetime import datetime, timezone

from models.database import SessionLocal 
from models.job import Job
from models.enums import JobStatus
from models.executions import Execution
from models.results import Result
from .queues import job_queue
from .handlers import JOB_HANDLERS

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to process a job by its ID
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
            started_at = datetime.now(timezone.utc),
            completed_at = None,
            error_message = None,
            error_category = None
        )
        job.status = JobStatus.RUNNING.value
        db.add(execution)
        db.commit()
        try:
            result = JOB_HANDLERS[job.job_type](job.payload)
        except Exception as e:
            execution.status = JobStatus.FAILED.value
            execution.completed_at = datetime.now(timezone.utc)
            job.status = JobStatus.FAILED.value
            execution.error_message = str(e)
            execution.error_category = "execution_failure"
            db.commit()
        else:
            result_entry = Result(
                result_id = uuid.uuid4(),
                job_id = job.job_id,
                execution_id = execution.execution_id,
                result_data = result,
                created_at = datetime.now(timezone.utc)
            )
            db.add(result_entry)
            db.commit()
            execution.status = JobStatus.COMPLETED.value
            execution.completed_at = datetime.now(timezone.utc)
            job.status = JobStatus.COMPLETED.value
            db.commit()
    finally:
        db.close()

# Function to run the worker loop that continuously processes jobs from the queue
def worker_loop():
    while True:
        try:
            job_id = job_queue.get()
            process_job(job_id)
        except Exception as e:
            print(f"Worker encountered an error: {e}")
    
