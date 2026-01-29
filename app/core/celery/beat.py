from app.core.celery.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "scan-pdf-every-1minute": {
        "task": "ingest_pdfs",
        "schedule": 60.0
    }
}

# celery -A app.core.celery.beat beat --loglevel=info

# Beat ──▶ Queue ──▶ Worker ──▶ Task function
# Beat = clock
# Queue = buffer (redis)
# Worker = executor
# Task = Python function
