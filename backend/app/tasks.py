import subprocess
from celery import Celery
from pathlib import Path
from .storage import s3, BUCKET_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.scene import Scene
import os
from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env.local")
load_dotenv()

OUTPUT_DIR = Path("renders")
OUTPUT_DIR.mkdir(exist_ok=True)

# broker and backend using redis
celery = Celery(
    "worker",
    # broker = "redis://localhost:6379/0",
    # backend = "redis://localhost:6379/0",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

#connecting to postgres database for scene data updation

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .models import Base
Base.metadata.create_all(bind=engine)

@celery.task
def render_scene(scene_id: int, code: str):
    """
    Runs a Manim script and saves output video.
    """
    script_path = OUTPUT_DIR / f"scene_{scene_id}.py"
    video_path = OUTPUT_DIR / f"scene_{scene_id}.mp4"

    script_path.write_text(code)

    subprocess.run(
        [
            "manim",
            "-ql",
            str(script_path.name),
            "ManimScene",  
            "-o",
            str(video_path.name)
        ],
        cwd=OUTPUT_DIR
    )

    # video path will be OUTPUT_DIR/media/videos/scene_id/480p15/scene_id.mp4
    video_path = OUTPUT_DIR / "media" / "videos" / f"scene_{scene_id}" / "480p15" / f"scene_{scene_id}.mp4"

    # uploading to s3 with content type video/mp4 in bucket name manim-videos with key scene_id.mp4
    s3.upload_file(str(video_path), BUCKET_NAME, f"scene_{scene_id}.mp4", ExtraArgs={"ContentType": "video/mp4"})

    #video url
    minio_endpoint = os.getenv("MINIO_ENDPOINT")
    video_url = f"{minio_endpoint}/{BUCKET_NAME}/scene_{scene_id}.mp4"

    # update database with video url
    db = SessionLocal()
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if scene:
        scene.video_url = video_url
        scene.status = "done"
        scene.code = code
        db.commit()
    db.close()

    # delete folder scene_id inside renders/media/videos directory delete even if not empty and no error if not exists
    import shutil
    shutil.rmtree(OUTPUT_DIR / "media" / "videos" / f"scene_{scene_id}", ignore_errors=True)

    # delete script file
    script_path.unlink(missing_ok=True)

    return {"status": "done", "video_path": str(video_path)}
