
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models.note import NoteCreate, NoteInDB, NoteUpdate
from app.config.db import Base


def create_note(db: Session, note: NoteCreate):
    db_note = NoteInDB(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note(db: Session, note_id: int):
    return db.query(NoteInDB).filter(NoteInDB.id == note_id).first()


def get_all_notes(db: Session):
    notes = db.query(NoteInDB).all()
    return [note.__dict__ for note in notes]


def update_note(db: Session, note_id: int, note: NoteUpdate):
    # Check if the note with the given ID exists
    db_note = get_note(db=db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update the note
    db.execute(
        update(NoteInDB).where(NoteInDB.id == note_id).values(
            title=note.title, desc=note.desc, important=note.important)
    )

    # Return the updated note
    updated_note = get_note(db=db, note_id=note_id)
    return updated_note


def delete_note(db: Session, note_id: int):
    deleted_note = get_note(db=db, note_id=note_id)
    if deleted_note:
        db.execute(delete(NoteInDB).where(NoteInDB.id == note_id))
        db.commit()
    return deleted_note
