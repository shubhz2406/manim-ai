celery -A app.tasks.celery worker --concurrency=1 --prefetch-multiplier=1 --loglevel=INFO -n worker1@%h
