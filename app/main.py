from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.note import NoteCreate, NoteOut, NoteUpdate
from app.CRUD.crud import create_note, get_note, get_all_notes, update_note, delete_note
from app.config.db import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from app.langchain.llm import llm_question_response

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/note_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/notes/", response_model=NoteOut)
def create_note_endpoint(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db=db, note=note)


@app.get("/notes/{note_id}", response_model=NoteOut)
def read_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    db_note = get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@app.get("/notes/all/", response_model=List[NoteOut])
def read_all_note_endpoint(db: Session = Depends(get_db)):
    db_notes = get_all_notes(db=db)
    return db_notes


@app.put("/notes/update/", response_model=NoteUpdate)
def update_note_endpoint(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    updated_note = update_note(db, note_id, note_update)
    return updated_note


@app.delete("/notes/delete/", response_model=NoteOut)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    # Check if the note with the given ID exists
    db_note = get_note(db=db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Delete the note
    deleted_note = delete_note(db=db, note_id=note_id)
    return deleted_note


@app.post("/notes/llm/")
def llm_response(item: dict):
    print(item)
    question = item.get("question")
    if not question:
        return {"error": "Missing 'question' in the request payload"}

    response = llm_question_response(question=question)
    return response
