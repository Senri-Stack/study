# url :https://fastapi.tiangolo.com/ja/tutorial/sql-databases/

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# datebase.pyからインポート
models.Base.metadata.create_all(bind=engine)