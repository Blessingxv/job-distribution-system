from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    worker_pool_size: int = 3

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_engine(settings.database_url, pool_size = 10, max_overflow = 20)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)