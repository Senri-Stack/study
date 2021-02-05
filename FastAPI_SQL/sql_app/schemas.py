from typing import List, Optional

from pydantic import BaseModel

# BaseModelを継承したクラスを作成
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

# BaseModelを継承したクラスをさらに継承　：作成用
class ItemCreate(ItemBase):
    pass

# BaseModelを継承したクラスをさらに継承　：読み込み用
class Item(ItemBase):
    id: int
    owner_id: int

    # Pydanticに設定を提供するために使用します。
    class Config:
        # データがdictではなくORMモデルであっても、Pydanticモデルにデータを読み込むように指示します。
        # データベースモデルから読み込み
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True