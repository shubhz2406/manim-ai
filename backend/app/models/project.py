from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    scene_ids = Column(ARRAY(Integer))
    user = relationship("User", back_populates="projects")
    scenes = relationship("Scene", back_populates="project")
