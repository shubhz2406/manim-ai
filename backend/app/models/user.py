from sqlalchemy import *
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    project_ids = Column(ARRAY(String))
    render_count = Column(Integer, default=0)
    projects = relationship("Project", back_populates="user")
