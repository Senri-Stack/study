# https://fastapi.tiangolo.com/tutorial/security/get-current-user/

from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

# 2:get_current_userは、我々が作成した（偽の）ユーティリティ関数を使用し、トークンをstrとして受け取り、Pydantic Userモデルを返します。
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

# 1:get_current_userは、以前に作成したのと同じoauth2_schemeとの依存関係を持っています。
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 2
    user = fake_decode_token(token)
    return user

# これで、パス操作でget_current_userと同じDependsを使うことができるようになりました。
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# これでパス操作機能で現在のユーザーを直接取得できるようになりました。