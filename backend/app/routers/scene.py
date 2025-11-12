from FastAPI import APIRouter
from pydantic import BaseModel
from ..tasks import render_scene
from ..database import SessionLocal
from ..models.scene import Scene
from google import genai

class SceneCreateRequest(BaseModel):
    prompt: str
    scene_id: int

router = APIRouter(
    prefix="/scene",
    tags=["scene"]
)

@router.post("/create-scene")
async def create_scene(request: SceneCreateRequest):
    db = SessionLocal()
    # Check if scene exists
    try:
        scene = db.query(Scene).filter(Scene.id == request.scene_id).first()
        if scene is None:
            return {"error": "Scene not found."}
    except Exception as e:
        return {"error": str(e)}
    
    scene = db.query(Scene).filter(Scene.id == request.scene_id).first()
    db.close()
    # if scene.code is not None: set make code variable to "" else to scene.code
    code = scene.code if scene.code is not None else ""
    if scene.code is None:
        content = request.prompt + "\nGenerate manim code for the above prompt. Only provide the code without any explanations. use config.frame_width = 16 and config.frame_height = 9. Give main scene name as ManimScene."
    else:
        content = request.prompt + "\nThe existing code is:\n" + code + "\nUpdate the above code based on the new prompt. Only provide the updated code without any explanations. Give main scene name as ManimScene."
    print("Generated content for GenAI:", content)

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=content
    )
    # slice responste to get only code block slice from python\n
    code_start = response.text.find("from manim import")
    code_end = response.text.rfind("```")
    generated_code = response.text[code_start:code_end] if code_start != -1 and code_end != -1 else "error: code not found in response"
    if generated_code.startswith("error"):
        return {"error": "Could not generate scene due to code extraction failure."}
    # Call render_scene task
    task = render_scene.delay(request.scene_id, generated_code)
    return {"task_id": task.id, "status": "queued", "generated_code": generated_code}

