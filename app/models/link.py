from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Link(Base):

    __tablename__ = "links"

    id = Column(Integer, primary_key=True)

    original_url = Column(String)
    short_code = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    clicks = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

