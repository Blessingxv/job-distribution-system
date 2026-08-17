from sqlalchemy import Column, Text, ForeignKey, Enum, VARCHAR, TIMESTAMP 
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .database import Base
import uuid

class Execution(Base):
    __tablename__ = "executions"

    execution_id = Column(UUID(as_uuid = True), primary_key = True, nullable = False, default = uuid.uuid4)
    job_id = Column(UUID(as_uuid = True), ForeignKey("jobs.job_id"), nullable = False)
    worker_id = Column(VARCHAR(50), nullable = True)
    status = Column(Enum("pending", "running", "completed", "failed", name = "executions_status"), nullable = False, default = "pending")
    started_at = Column(TIMESTAMP(timezone = True), nullable = True, default = lambda: datetime.now(timezone.utc))
    completed_at = Column(TIMESTAMP(timezone = True), nullable = True, default = lambda: datetime.now(timezone.utc))
    error_message = Column(Text, nullable = True)
    error_category = Column(VARCHAR(50), nullable = True)