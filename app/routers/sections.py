# app/routers/section.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sections import Section
from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse

router = APIRouter(prefix="/sections", tags=["Sections"])


# -------------------------------------------------------------
# CREATE SECTION
# -------------------------------------------------------------
@router.post("/", response_model=SectionResponse)
def create_section(section_data: SectionCreate, db: Session = Depends(get_db)):

    # Check duplicate name
    existing = db.query(Section).filter(Section.name == section_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Section name already exists.")

    new_section = Section(name=section_data.name)
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section


# -------------------------------------------------------------
# GET ALL SECTIONS
# -------------------------------------------------------------
@router.get("/", response_model=list[SectionResponse])
def get_all_sections(db: Session = Depends(get_db)):
    return db.query(Section).all()


# -------------------------------------------------------------
# GET SECTION BY ID
# -------------------------------------------------------------
@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(Section).filter(Section.id == section_id).first()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    return section


# -------------------------------------------------------------
# UPDATE SECTION
# -------------------------------------------------------------
@router.put("/{section_id}", response_model=SectionResponse)
def update_section(section_id: int, section_data: SectionUpdate, db: Session = Depends(get_db)):

    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Check duplicate (other section with same name)
    existing = db.query(Section).filter(
        Section.name == section_data.name,
        Section.id != section_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Section name already exists.")

    section.name = section_data.name
    db.commit()
    db.refresh(section)

    return section


# -------------------------------------------------------------
# DELETE SECTION
# -------------------------------------------------------------
@router.delete("/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db)):

    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    db.delete(section)
    db.commit()

    return {"message": "Section deleted successfully"}
