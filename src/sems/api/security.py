"""
احراز هویت JWT ساده برای API.

⚠️ توجه امنیتی: این یک جایگزین نمایشی برای الزام «احراز هویت چندمرحله‌ای»
بخش ۲-۵-۲ SRS است، نه پیاده‌سازی کامل MFA سازمانی. رمزنگاری انتقال (TLS 1.3)
نیز باید در لایه استقرار (reverse proxy / ingress) تأمین شود، نه در این کد.
برای استفاده واقعی: SEMS_JWT_SECRET را به یک مقدار تصادفی قوی تنظیم کنید و
کاربران را از یک منبع هویت واقعی (نه env var) احراز کنید.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

JWT_SECRET = os.environ.get("SEMS_JWT_SECRET", "dev-only-insecure-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DEMO_USERNAME = os.environ.get("SEMS_API_USERNAME", "operator")
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_DEFAULT_DEMO_PASSWORD_HASH = _pwd_context.hash("changeme")
DEMO_PASSWORD_HASH = os.environ.get("SEMS_API_PASSWORD_HASH", _DEFAULT_DEMO_PASSWORD_HASH)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str) -> bool:
    if username != DEMO_USERNAME:
        return False
    return _pwd_context.verify(password, DEMO_PASSWORD_HASH)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="اعتبارسنجی توکن ناموفق بود",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_error
        return username
    except JWTError as exc:
        raise credentials_error from exc
