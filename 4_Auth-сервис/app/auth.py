from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import redis

load_dotenv()

# Настройки JWT
# JWT settings
# 使用固定的密钥以确保一致性
# Use fixed secret key for consistency
SECRET_KEY = "my-super-secret-key-for-student-project-that-is-long-enough-for-jwt-1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Контекст для хэширования паролей
# Context for password hashing
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception as e:
    print(f"警告: 创建密码上下文时出错: {e}")
    # 备用方案
    # Fallback solution
    from passlib.hash import bcrypt_sha256
    pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# Подключение к Redis
# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    # Verifies password
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"密码验证错误: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Хэширует пароль"""
    # Hashes password
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает access токен"""
    # Creates access token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"[DEBUG] Создан access token: {encoded_jwt[:50]}...")
        return encoded_jwt
    except Exception as e:
        print(f"[ERROR] Ошибка создания access token: {e}")
        raise

def create_refresh_token(data: dict):
    """Создает refresh токен"""
    # Creates refresh token
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"[DEBUG] Создан refresh token: {encoded_jwt[:50]}...")
        return encoded_jwt
    except Exception as e:
        print(f"[ERROR] Ошибка создания refresh token: {e}")
        raise

def verify_token(token: str):
    """Проверяет JWT токен"""
    # Verifies JWT token
    try:
        print(f"[DEBUG] Начало проверки токена: {token[:30]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[DEBUG] Токен проверен успешно: user_id={payload.get('sub')}, type={payload.get('type')}")
        return payload
    except JWTError as e:
        print(f"[DEBUG] Ошибка проверки токена (JWTError): {e}")
        return None
    except Exception as e:
        print(f"[DEBUG] Ошибка проверки токена (Exception): {e}")
        return None

def add_to_blacklist(token: str, expire_seconds: int):
    """Добавляет токен в черный список (Redis)"""
    # Adds token to blacklist (Redis)
    try:
        redis_client.setex(f"blacklist:{token}", expire_seconds, "true")
        print(f"[DEBUG] Токен добавлен в черный список: {token[:30]}...")
    except Exception as e:
        print(f"[ERROR] Ошибка добавления в черный список: {e}")

def is_token_blacklisted(token: str) -> bool:
    """Проверяет, находится ли токен в черном списке"""
    # Checks if token is in blacklist
    try:
        result = redis_client.exists(f"blacklist:{token}") == 1
        if result:
            print(f"[DEBUG] Токен найден в черном списке: {token[:30]}...")
        return result
    except Exception as e:
        print(f"[ERROR] Ошибка проверки черного списка: {e}")
        return False