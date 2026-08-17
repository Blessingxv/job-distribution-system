from sqlalchemy import Column, Enum, Integer, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(UUID(as_uuid = True), primary_key = True, nullable = False, default = uuid.uuid4)
    job_type = Column(VARCHAR(50), nullable = False)
    payload = Column(JSONB, nullable = False)
    priority = Column(Integer, nullable = False, default = 0)
    status = Column(Enum("pending", "running", "completed", "failed", name = "job_status"), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, default = lambda: datetime.now(timezone.utc))
    updated_at = Column(
        TIMESTAMP(timezone = True), 
        nullable = False, 
        default = lambda: datetime.now(timezone.utc), 
        onupdate = lambda: datetime.now(timezone.utc))
    max_retries = Column(Integer, nullable = False, default = 3)