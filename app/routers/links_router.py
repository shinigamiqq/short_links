from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.link import CreateLink, UpdateLink
from app.services.link_service import create_link, get_original_url, increment_click
from app.models.link import Link

router = APIRouter(prefix="/links")


@router.post("/shorten")
def shorten_link(data: CreateLink, db: Session = Depends(get_db)):

    link = create_link(
        db,
        data.original_url,
        data.custom_alias,
        data.expires_at
    )

    return {"short_url": f"http://localhost:8000/{link.short_code}"}


@router.get("/search")
def search(original_url: str, db: Session = Depends(get_db)):

    links = db.query(Link).filter(Link.original_url == original_url).all()

    return links


@router.delete("/{short_code}")
def delete_link(short_code: str, db: Session = Depends(get_db)):

    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(404)

    db.delete(link)
    db.commit()

    return {"status": "deleted"}


@router.put("/{short_code}")
def update_link(short_code: str, data: UpdateLink, db: Session = Depends(get_db)):

    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(404)

    link.original_url = data.original_url
    db.commit()

    return {"status": "updated"}


@router.get("/{short_code}/stats")
def stats(short_code: str, db: Session = Depends(get_db)):

    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(404)

    return link

