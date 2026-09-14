import threading
import pytest
import time
from workers.worker import process_job
from models.database import SessionLocal
from models.job import Job
from models.enums import JobStatus
from models.results import Result
from models.executions import Execution


def test_process_job_concurrent():
    session = SessionLocal()

    # Creation of 5 jobs with known expected results
    jobs_data = [
        ("beam_calculation", {
            "length": 1000,
            "load": 1000,
            "load_position": 500,
            "second_moment_of_area": 8333333.33,
            "extreme_fiber_distance": 50
            }, {"result": 1.5}),
        ("fibonacci", {"n": 10}, {"result": 55}),
        ("fibonacci", {"n": 0}, {"result": 0}),
        ("prime_check", {"n": 7}, {"result": True}),
        ("prime_check", {"n": 8}, {"result": False}),
    ]

    job_ids = []
    for job_type, payload, expected in jobs_data:
        job = Job(job_type = job_type, payload = payload, status = JobStatus.PENDING.value)
        session.add(job)
        session.commit()
        job_ids.append((job.job_id, expected))

    # Run all 5 concurrently
    errors = []

    def run_and_capture(job_id):
        try:
            process_job(job_id)
        except Exception as e:
            errors.append((job_id, e))

    threads = []
    for job_id, expected in job_ids:
        t = threading.Thread(target = run_and_capture, args = (job_id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    session.expire_all() 

    assert not errors, f"Exceptions occurred during concurrent processing: {errors}"

    # Checking each job's specific result
    for job_id, expected in job_ids:
        job_row = session.query(Job).filter_by(job_id = job_id).first()
        print(f"job_id = {job_id}, job_type = {job_row.job_type}, status  ={job_row.status}")
        assert job_row.status == JobStatus.COMPLETED.value

        result_row = session.query(Result).filter_by(job_id = job_id).first()
        assert result_row is not None

        actual_value = result_row.result_data["result"]
        expected_value = expected["result"]

        if isinstance(actual_value, float):
            assert round(actual_value, 2) == round(expected_value, 2)
        else:
            assert actual_value == expected_value

    # Cleanup by deleting child rows first, then parent
    for job_id, expected in job_ids:
        result_row = session.query(Result).filter_by(job_id = job_id).first()
        if result_row:
            session.delete(result_row)
            session.commit()

        execution_row = session.query(Execution).filter_by(job_id=job_id).first()
        if execution_row:
            session.delete(execution_row)
            session.commit()

        job_row = session.query(Job).filter_by(job_id = job_id).first()
        session.delete(job_row)
        session.commit()

    session.close()
