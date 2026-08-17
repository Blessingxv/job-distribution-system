from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
from .database import Base
import uuid

class Result(Base):
    __tablename__ = "results"

    result_id = Column(UUID(as_uuid = True), primary_key = True, nullable = False, default = uuid.uuid4)
    job_id = Column(UUID(as_uuid = True), ForeignKey("jobs.job_id"), nullable = False)
    execution_id = Column(UUID(as_uuid = True), ForeignKey("executions.execution_id"), nullable = False)
    result_data = Column(JSONB, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, default = lambda: datetime.now(timezone.utc))