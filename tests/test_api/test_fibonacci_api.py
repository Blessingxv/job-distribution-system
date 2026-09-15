import uuid

from fastapi.testclient import TestClient
from api.main import app
from models.database import SessionLocal
from models.job import Job
from models.enums import JobStatus


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