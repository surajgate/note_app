from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from app.config.db import Base

class NoteInDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    desc = Column(String)
    important = Column(Boolean)

class NoteCreate(BaseModel):
    title: str
    desc: str
    important: bool

class NoteUpdate(BaseModel):
    title: str
    desc: str
    important: bool

class NoteOut(BaseModel):
    id: int
    title: str
    desc: str
    important: bool