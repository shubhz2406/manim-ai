from fastapi import FastAPI
from .tasks import render_scene
from pydantic import BaseModel
from .routers import scenc as scene_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

class RenderRequest(BaseModel):
    code: str

app.include_router(scene_router.router)

@app.post("/render/{scene_id}")
def create_render(scene_id: int, request: RenderRequest):
    task = render_scene.delay(scene_id, request.code)  # enqueue task
    return {"task_id": task.id, "status": "queued"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    from .tasks import celery
    result = celery.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}



