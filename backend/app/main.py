from fastapi import FastAPI
from .tasks import render_scene
from pydantic import BaseModel
from .database import Base, engine, SessionLocal
from .models.user import User
from .models.project import Project
from .models.scene import Scene

# Base.metadata.create_all(bind=engine)

# dummy user code
# db = SessionLocal()
# user = User(email="user@example.com", name="John Doe", hashed_password="hashedpassword", projects=[], render_count=0)
# db.add(user)
# db.commit()
# db.refresh(user)

# project = Project(name="Demo Project", owner_id=user.id, scene_ids=[])
# db.add(project)
# db.commit()
# db.refresh(project)

# scene = Scene(name="Demo Scene 2", project_id=1, status="queued", video_url="", image_url="", code="", chat=[])
# db.add(scene)
# db.commit()         
# db.refresh(scene)

# print(f"Created scene: {scene.name}")

# db.close()



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class RenderRequest(BaseModel):
    code: str

@app.post("/render/{scene_id}")
def create_render(scene_id: int, request: RenderRequest):
    task = render_scene.delay(scene_id, request.code)  # enqueue task
    return {"task_id": task.id, "status": "queued"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    from .tasks import celery
    result = celery.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}
