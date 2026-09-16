# Distributed Job Processing System

A scheduler, queue and worker system built in Python with FastAPI and PostgreSQL. Clients submit jobs through a REST API, jobs are queued and picked up by a pool of concurrent worker threads, and results are persisted and retrievable through the API.

This project was built after completing Harvard's CS50W to demonstrate backend and distributed systems fundamentals which include queuing, concurrency, persistence, failure handling, automated testing, CI, and containerization.

## Features

- REST API for submitting jobs, checking job status and retrieving results
- In process job queue with a configurable pool of worker threads
- Three supported job types: fibonacci, prime_check and beam_calculation (a real engineering calculation reused from an earlier capstone project)
- Job lifecycle tracking (queued, running, completed, failed) backed by PostgreSQL
- Structured error handling with distinct failure categories
- Full automated test suite: unit tests, integration tests, API tests and a concurrency test
- Continuous integration via GitHub Actions, running the full test suite against a real PostgreSQL service container on every push
- Fully containerized with Docker and Docker Compose

## Architecture

Client -> REST API (FastAPI) -> Job Queue -> Worker Threads -> PostgreSQL

The API validates and persists incoming jobs, then places them on an in memory queue. 
A configurable number of worker threads pull jobs off the queue, execute the matching handler function and write the outcome back to the database. 
Workers run inside the same process as the API, started through FastAPI's lifespan hook.

### Data model

- **Job**: the unit of work submitted by a client. Tracks its own overall status.
- **Execution**: one attempt at running a job. A job can have more than one execution if retries are introduced later.
- **Result**: the output of a successful execution.

A job only reaches a completed status once its result has actually been persisted. Nothing is reported as done prematurely.

### Job types

Job types are restricted to a fixed whitelist mapped to pre-registered handler functions. Clients cannot submit arbitrary code to be executed, only one of the supported job types with a validated payload.

- fibonacci: computes the nth Fibonacci number
- prime_check: checks whether a number is prime
- beam_calculation: computes reactions, bending moment and bending stress for a simply supported beam under a single point load

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/jobs | Submit a new job |
| GET | /api/v1/jobs/{job_id} | Get the status of a job |
| GET | /api/v1/jobs/{job_id}/result | Get the result of a completed job |

Interactive API documentation is available at `/docs` once the app is running.

## Running locally with Docker

This is the fastest way to run the whole system, since it starts both the app and a PostgreSQL database with no manual setup.

docker compose up --build

Once running, the API is available at `http://localhost:8000` and the health check at `http://localhost:8000/health`.

## Running locally without Docker

Requirements: Python 3.13 and a running PostgreSQL instance.

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a `.env` file in the project root with your database connection string:

DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database>

Create the database tables:

python -m models.create_model

Start the app:

uvicorn api.main:app --reload

## Running the tests

pytest tests/ -v

The test suite covers individual job handlers, the queue and worker pipeline end to end, concurrent job processing and the API's behavior including validation and error responses.

## Continuous integration

Every push and pull request to main triggers a GitHub Actions workflow that spins up a real PostgreSQL container, creates the database tables, and runs the full test suite. The workflow definition lives in `.github/workflows/tests.yml`.

## Project structure

api/          FastAPI app, routes and Pydantic schemas
models/       SQLAlchemy models and database setup
workers/      Job queue, worker loop and job handlers
tests/        Unit, integration and API tests
Dockerfile
docker-compose.yml

## Design decisions

A few decisions worth calling out for anyone reviewing this project:

- **Threads over processes.** Worker concurrency uses Python threads rather than multiprocessing, since the workloads here are not CPU bound enough to need process level parallelism, and threads keep the implementation simpler.
- **A fixed job type whitelist.** Job types map to specific, pre-registered handler functions rather than accepting arbitrary code, closing off an entire class of security risk.
- **Retry logic deliberately left out for now.** The only failure category the system currently produces is deterministic: the same bad input always fails the same way, so retrying would never change the outcome. Retry and requeue logic will be added once a genuinely transient failure category exists, for example a job type that depends on an external service.
- **Tests run against a real PostgreSQL database rather than SQLite or mocks**, both locally and in CI, so the tests reflect how the system actually behaves in production.

## What is out of scope

This is a portfolio project with a deliberately bounded MVP. Authentication, multi tenancy, horizontal scaling across machines and production grade monitoring are all out of scope for now. A scalability path (message broker, multiple worker machines, shared result storage) is documented in the project's design notes for future extension.

## Author

Built by [Blessing](https://github.com/Blessingxv).
