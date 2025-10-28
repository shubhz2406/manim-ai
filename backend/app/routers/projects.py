from fastapi import APIRouter,httpException,Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal 

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

#GET projects route
@router.get("/")
def get_projects(db: Session = Depends(SessionLocal)):
    projects = db.query(models.Project).all()
    return projects

#POST create project route
@router.post("/")
def add_project(name: str, owner_id: int, db: Session = Depends(SessionLocal)):
    new_project = models.Project(name=name, owner_id=owner_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

#GET project by ID route
@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(SessionLocal)):  
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise httpException(status_code=404, detail="Project not found")
    return project

#DELETE project by ID route
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise httpException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted"}

#PUT update project route
@router.put("/{project_id}")
def update_project(project_id: int, name: str = None, db: Session = Depends(SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise httpException(status_code=404, detail="Project not found")
    if name:
        project.name = name
    db.commit()
    db.refresh(project)
    return project

#Add scene to project route with scene name in request body
@router.post("/{project_id}/scene/")
def add_scene_to_project(project_id: int, scene_name: str, db: Session = Depends(SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise httpException(status_code=404, detail="Project not found")
    new_scene = models.Scene(name=scene_name, project_id=project.id)
    db.add(new_scene)
    db.commit()
    db.refresh(new_scene)
    return new_scene

#Delete scene from project route
@router.delete("/{project_id}/scene/{scene_id}")
def delete_scene_from_project(project_id: int, scene_id: int, db: Session = Depends(SessionLocal)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise httpException(status_code=404, detail="Project not found")
    scene = db.query(models.Scene).filter(models.Scene.id == scene_id, models.Scene.project_id == project_id).first()
    if not scene:
        raise httpException(status_code=404, detail="Scene not found in this project")
    db.delete(scene)
    db.commit()
    return {"detail": "Scene deleted from project"}

