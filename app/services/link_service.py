from sqlalchemy.orm import Session
from datetime import datetime
from app.models.link import Link
from app.utils.shortener import generate_code
from app.redis_client import redis_client


def create_link(db: Session, original_url, alias=None, expires_at=None):

    code = alias if alias else generate_code()

    link = Link(
        original_url=original_url,
        short_code=code,
        expires_at=expires_at
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    return link


def get_original_url(db: Session, code: str):

    cached = redis_client.get(code)

    if cached:
        return cached

    link = db.query(Link).filter(Link.short_code == code).first()

    if not link:
        return None

    redis_client.set(code, link.original_url)

    return link.original_url


def increment_click(db: Session, code: str):

    link = db.query(Link).filter(Link.short_code == code).first()

    if link:
        link.clicks += 1
        link.last_used = datetime.utcnow()

        db.commit()

