from fastapi import APIRouter
from app.models.note import Note
# from config.db import
from app.schema.note import noteEntity, notesEntity

note = APIRouter()
