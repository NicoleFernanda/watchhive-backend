from fastapi import APIRouter, BackgroundTasks,Depends
from db.database import get_db, SessionLocal
from models.midia import Midia
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session


midia_router = APIRouter(
    prefix="/midias",
    tags=["midia"],
)

@midia_router.get("/", response_model=list[Midia])
def create_genres(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task()


@midia_router.get("/create", response_model=bool)
def create(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task()
