from models.database import SessionLocal
from models.job import Job
from models.enums import JobStatus
from workers.worker import process_job
from models.executions import Execution
from models.results import Result


def test_process_job_fibonacci_success():
    # Creating and committing a real job
    session = SessionLocal()
    job = Job(job_type = "fibonacci", payload = {"n": 10}, status = JobStatus.PENDING.value)
    session.add(job)
    session.commit()
    job_id = job.job_id

    # Call process_job
    process_job(job_id)

    # requery fresh state and check results
    session.refresh(job)
    assert job.status == JobStatus.COMPLETED.value

    execution = session.query(Execution).filter_by(job_id=job_id).first()
    assert execution is not None
    assert execution.status == JobStatus.COMPLETED.value

    result = session.query(Result).filter_by(job_id=job_id).first()
    assert result is not None
    assert result.result_data == {"result": 55}

    # Cleanup by deleting child rows first, then parent
    session.delete(result)
    session.commit()
    session.delete(execution)
    session.commit()
    session.delete(job)
    session.commit()
    session.close()

def test_process_job_fibonacci_fail():
    # Creating and committing a real job
    session = SessionLocal()
    job = Job(job_type = "fibonacci", payload = {"n": -1}, status = JobStatus.PENDING.value)
    session.add(job)
    session.commit()
    job_id = job.job_id

    # Call process_job
    process_job(job_id)

    # requery fresh state and check results
    session.refresh(job)
    assert job.status == JobStatus.FAILED.value

    execution = session.query(Execution).filter_by(job_id=job_id).first()
    assert execution is not None
    assert execution.status == JobStatus.FAILED.value

    assert execution.error_message is not None
    assert execution.error_category is not None

    # Cleanup by deleting child rows first, then parent
    session.delete(execution)
    session.commit()
    session.delete(job)
    session.commit()
    session.close()