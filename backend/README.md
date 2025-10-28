Backend Server : 
    -> run the fastapi app in terminal 1 using cmd : uvicorn app.main:app --reload --reload-exclude "renders/*"

Celery worker : 
    -> run this command in terminal 2 : celery -A app.tasks.celery worker --concurrency=1 --prefetch-multiplier=1 --loglevel=INFO 

    

Both the above while in backend folder.

