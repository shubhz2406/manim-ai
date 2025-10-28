from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String, default="queued")
    video_url = Column(String)
    image_url = Column(String)
    code = Column(String)
    chat = Column(ARRAY(String))
    project = relationship("Project", back_populates="scenes")
