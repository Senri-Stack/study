from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# クライアント (ユーザーのブラウザで動作するフロントエンド) がトークンを取得するためにユーザー名とパスワードを送信するURLを指定する。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
# oauth2_schemeをDependsで依存関係に渡すことができる。
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}