import uuid

from fastapi.testclient import TestClient
from api.main import app
from models.database import SessionLocal
from models.job import Job
from models.enums import JobStatus
from models.executions import Execution
from models.results import Result
from datetime import datetime, timezone


client = TestClient(app)

def test_create_job_fibonacci():
    session = SessionLocal()

    # Job creating and expected response
    response = client.post("/api/v1/jobs", json = {
        "job_type": "fibonacci",
        "payload": {"n": 10}
    })

    assert response.status_code == 200
    data = response.json()
    assert data["job_type"] == "fibonacci"
    assert data["status"] == "pending"

    job_id = data["job_id"]

    
    job_row = session.query(Job).filter_by(job_id = job_id).first()
    assert job_row is not None
    assert job_row.status == JobStatus.PENDING.value
    assert job_row.payload == {"n": 10}

    # Cleanup
    session.delete(job_row)
    session.commit()
    session.close()

def test_get_job_fibonacci_happy_path():
    session = SessionLocal()

    # Job creation
    job = Job(job_type = "fibonacci", payload = {"n": 10}, status = JobStatus.PENDING.value)
    session.add(job)
    session.commit()
    job_id = job.job_id

    # Expected response
    response = client.get(f"/api/v1/jobs/{job_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == str(job_id)
    assert data["job_type"] == "fibonacci"
    assert data["status"] == "pending"

    # Query job row
    job_row = session.query(Job).filter_by(job_id = job_id).first()
    assert job_row is not None
    assert job_row.status == JobStatus.PENDING.value
    assert job_row.payload == {"n": 10}

    # Cleanup
    session.delete(job_row)
    session.commit()
    session.close()

def test_get_job_fibonacci_404():
    fake_job_id = uuid.uuid4()

    response = client.get(f"/api/v1/jobs/{fake_job_id}")

    assert response.status_code == 404

def test_get_job_result_fibonacci():
    session = SessionLocal()

    # Job creation
    job = Job(job_type = "fibonacci", payload = {"n": 10}, status = JobStatus.COMPLETED.value)
    session.add(job)
    session.commit()
    job_id = job.job_id

    # Execution creation
    execution = Execution(
        job_id = job_id,
        worker_id = "test-worker",
        status = JobStatus.COMPLETED.value,
        started_at = datetime.now(timezone.utc),
        completed_at = datetime.now(timezone.utc),
    )
    session.add(execution)
    session.commit()
    execution_id = execution.execution_id

    # Result creation
    result_row = Result(
        job_id = job_id,
        execution_id = execution_id,
        result_data = {"result": 55},
    )
    session.add(result_row)
    session.commit()

    # Query job row
    job_row = session.query(Job).filter_by(job_id = job_id).first()
    assert job_row is not None
    assert job_row.status == JobStatus.COMPLETED.value
    assert job_row.payload == {"n": 10}

    # Query execution row
    execution_row = session.query(Execution).filter_by(job_id = job_id).first()
    assert execution_row is not None
    assert execution_row.status == JobStatus.COMPLETED.value

    result_row = session.query(Result).filter_by(job_id = job_id).first()
    assert result_row is not None
    assert result_row.result_data == {"result": 55}
    
    # Expected response
    response = client.get(f"/api/v1/jobs/{job_id}/result")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == str(job_id)
    assert data["job_type"] == "fibonacci"
    assert data["status"] == "completed"

    # Cleanup by deleting child rows first, then parent
    session.delete(result_row)
    session.commit()
    session.delete(execution)
    session.commit()
    session.delete(job)
    session.commit()
    session.close()

def test_get_job_result_fibonacci_404():
    fake_job_id = uuid.uuid4()

    response = client.get(f"/api/v1/jobs/{fake_job_id}/result")

    assert response.status_code == 404

def test_get_job_result_fibonacci_409():
    session = SessionLocal()

    # Job creation - still running, no result yet
    job = Job(job_type="fibonacci", payload={"n": 10}, status=JobStatus.RUNNING.value)
    session.add(job)
    session.commit()
    job_id = job.job_id

    # Expected response
    response = client.get(f"/api/v1/jobs/{job_id}/result")

    assert response.status_code == 409

    # Cleanup
    session.delete(job)
    session.commit()
    session.close()
