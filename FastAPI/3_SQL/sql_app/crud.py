# sqlalchemy.ORMからSessionをインポート
from sqlalchemy.orm import Session
# モデル（SQLAlchemyモデル）とスキーマ（Pydanticモデル/スキーマ）をインポート
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# データを作成する
def create_user(db: Session, user: schemas.UserCreate):
    # SQLAlchemyモデルのインスタンスをデータと共に作成します。
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # インスタンスオブジェクトをデータベースセッションに追加します。
    db.add(db_user)
    # 変更をデータベースにコミットします
    db.commit()
    # インスタンスをリフレッシュします（生成された ID のようなデータベースからの新しいデータが含まれるように）。
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item