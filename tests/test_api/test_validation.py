from fastapi.testclient import TestClient
from api.main import app
from models.database import SessionLocal
from models.job import Job

client = TestClient(app)


def test_create_job_prime_check_valid():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "prime_check",
        "payload": {"n": 7}
    })
    assert response.status_code == 200
    session = SessionLocal()
    job = session.query(Job).filter_by(job_id = response.json()["job_id"]).first()
    session.delete(job)
    session.commit()
    session.close()


def test_create_job_prime_check_missing_n():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "prime_check",
        "payload": {}
    })
    assert response.status_code == 422


def test_create_job_prime_check_wrong_type():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "prime_check",
        "payload": {"n": "seven"}
    })
    assert response.status_code == 422


def test_create_job_prime_check_bool_rejected():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "prime_check",
        "payload": {"n": True}
    })
    assert response.status_code == 422


def test_create_job_prime_check_out_of_range():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "prime_check",
        "payload": {"n": 1}
    })
    assert response.status_code == 422


def test_create_job_beam_calculation_valid():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "beam_calculation",
        "payload": {
            "length": 1000,
            "load": 1000,
            "load_position": 500,
            "second_moment_of_area": 8333333.33,
            "extreme_fiber_distance": 50
        }
    })
    assert response.status_code == 200
    session = SessionLocal()
    job = session.query(Job).filter_by(job_id = response.json()["job_id"]).first()
    session.delete(job)
    session.commit()
    session.close()


def test_create_job_beam_calculation_missing_field():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "beam_calculation",
        "payload": {
            "length": 1000,
            "load": 1000,
            "load_position": 500,
            "second_moment_of_area": 8333333.33
            # extreme_fiber_distance missing
        }
    })
    assert response.status_code == 422


def test_create_job_beam_calculation_load_position_out_of_range():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "beam_calculation",
        "payload": {
            "length": 1000,
            "load": 1000,
            "load_position": 1500, 
            "second_moment_of_area": 8333333.33,
            "extreme_fiber_distance": 50
        }
    })
    assert response.status_code == 422


def test_create_job_beam_calculation_negative_value():
    response = client.post("/api/v1/jobs", json = {
        "job_type": "beam_calculation",
        "payload": {
            "length": 1000,
            "load": -1000,  # negative, invalid
            "load_position": 500,
            "second_moment_of_area": 8333333.33,
            "extreme_fiber_distance": 50
        }
    })
    assert response.status_code == 422