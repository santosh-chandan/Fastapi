from app.core.celery.celery_app import celery_app

# Celery discovers tasks by:
# Importing modules
# Registering @celery_app.task
# If the module is never imported, the task does not exist.
# so just import as module only - it will explore all tasks and register.
import app.core.celery.tasks

# this worker will run only this way
    # celery -A app.core.celery.worker worker --loglevel=info

# 1. celery is cli tools to execute through celery.
# 2. now need our celery configs - this is the path for celery_app - app.core.celery.worker
    # Import this Python module so Celery can find a Celery app instance with custom configuration.
# 3. worker - This is the Celery command, not a filename. - means: “Start a worker process that consumes tasks”
