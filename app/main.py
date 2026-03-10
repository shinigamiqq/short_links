from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.link_service import get_original_url, increment_click
from app.routers.links_router import router as links_router

from app.models import user
from app.models import link

from app.database import Base, engine
import app.models


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(links_router)


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    url = get_original_url(db, short_code)

    if not url:
        return {"error": "not found"}

    increment_click(db, short_code)

    return RedirectResponse(url)

