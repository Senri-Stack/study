# パスワードのハッシュ（暗号）化
# URL : https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# 1.Install passlib : pip install passlib[bcrypt]

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 「受信したパスワード」が「保存されているハッシュ」と一致するかどうかを確認する。
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# パスワードをハッシュ化
def get_password_hash(password):
    return pwd_context.hash(password)

# ユーザを認証して返す。
def authenticate_user(fake_db, username: str, password: str):
    # ユーザー情報をDBから取得している。
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user