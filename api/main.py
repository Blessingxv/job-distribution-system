import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from .routes import router
from workers.worker import worker_loop
from models.database import settings

# Lifespan context manager to start worker threads when the FastAPI app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start worker threads to process jobs from queue
    for i in range(settings.worker_pool_size): 
        try:
            worker_thread = threading.Thread(target = worker_loop).start()
        except Exception as e:
            print(f"Error starting worker thread: {e}")
    yield
    # Shutdown code goes here

app = FastAPI(lifespan = lifespan)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}