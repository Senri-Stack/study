from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
# OAuth2PasswordRequestFormをインポート
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# このユーザがアクティブな場合にのみ、current_userを取得するため、get_current_active_userという追加の依存関係を作成し、 get_current_userを依存関係として使用します。
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # ユーザーが存在しない場合やアクティブでない場合にHTTPエラーを返すだけです。
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
# /tokenのパス操作でDependsを使って依存関係として使用します。
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # フォームフィールドのユーザー名を使って、データベースからユーザーデータを取得し、該当ユーザがいない場合は、"不正なユーザ名またはパスワード "というエラーを返します。
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # パスワードハッシュシステムを使用して、パスワードが一致しない場合は同じエラーを返します。
    user = UserInDB(**user_dict) # user_dictのキーと値を直接キー-値の引数として渡します。
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
    # 仕様では、access_tokenとtoken_typeを持つJSONを返すことになっています。
    # これはコードの中で自分でやらなければならないことで、それらのJSONキーを使うようにしてください。


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user