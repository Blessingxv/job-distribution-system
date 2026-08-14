from .job import Job
from .database import Base, engine

Base.metadata.create_all(engine)