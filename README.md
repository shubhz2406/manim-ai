## Setup the project
> Create .env file in root folder refer .env.example

> Backend Server : 
    > run the fastapi app in terminal 1 using cmd : 
    uvicorn app.main:app --reload --reload-exclude "renders/*"

Celery worker : 
    -> run this command in terminal 2 : 
    celery -A app.tasks.celery worker --concurrency=1 --prefetch-multiplier=1 --loglevel=INFO 


Both the above while in backend folder, in a virtual env.

Run docker-compose up --build while in root folder to get redis, postgres, minio setup via docker.

Need to do migrations to using alembic. Steps Below : 
    -> Start backend server and postgres db.
    -> run "alembic init alembic" in apps folder
    -> in alembic.ini created update the sqlalchemy.url update your db url
    -> update enp.py in 



