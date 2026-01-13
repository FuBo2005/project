from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from . import auth, schemas, models
from .database import get_db

router = APIRouter()
security = HTTPBearer()

# Модель для отладки токенов
# Model for token debugging
class DebugTokenRequest(BaseModel):
    token: str

# Эндпоинт для отладки токенов
# Endpoint for token debugging
@router.post("/debug-token")
async def debug_token(request: DebugTokenRequest):
    """Отладка токенов"""
    # Token debugging
    token = request.token
    
    # Проверяем токен
    # Verify token
    payload = auth.verify_token(token)
    
    if payload:
        return {
            "valid": True,
            "payload": payload,
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "type": payload.get("type"),
            "exp": payload.get("exp"),
            "exp_datetime": datetime.fromtimestamp(payload.get("exp")) if payload.get("exp") else None
        }
    else:
        return {
            "valid": False, 
            "message": "Token verification failed"
        }

# Регистрация пользователя
# User registration
@router.post("/register", response_model=schemas.MessageResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    # Registration of new user
    
    # Проверяем, существует ли пользователь
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Создаем нового пользователя
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Пользователь успешно зарегистрирован"}

# Вход в систему
# Login
@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    """Авторизация пользователя"""
    # User authorization
    
    # Ищем пользователя
    # Find user
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Записываем историю входа
    # Record login history
    login_history = models.LoginHistory(
        user_id=db_user.id,
        user_agent=request.headers.get("user-agent")
    )
    db.add(login_history)
    db.commit()
    
    # Создаем токены
    # Create tokens
    token_data = {"sub": str(db_user.id), "email": db_user.email}
    access_token = auth.create_access_token(data=token_data)
    refresh_token = auth.create_refresh_token(data=token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Обновление токенов
# Token refresh
@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh(token_data: schemas.TokenRefresh):
    """Обновление access токена"""
    # Refresh access token
    
    # Проверяем refresh токен
    # Verify refresh token
    payload = auth.verify_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh токен"
        )
    
    # Проверяем, не в черном списке ли токен
    # Check if token is blacklisted
    if auth.is_token_blacklisted(token_data.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен"
        )
    
    # Создаем новый access токен
    # Create new access token
    new_access_token = auth.create_access_token(
        data={"sub": payload["sub"], "email": payload["email"]}
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": token_data.refresh_token,  # Тот же refresh токен
        "token_type": "bearer"
    }

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Получает текущего пользователя из токена"""
    # Gets current user from token
    
    token = credentials.credentials
    
    # Отладочная информация
    # Debug information
    print(f"[DEBUG] Проверка токена: {token[:30]}...")
    
    # Проверяем токен
    # Verify token
    payload = auth.verify_token(token)
    print(f"[DEBUG] Результат проверки токена: {payload}")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен (проверка не удалась)"
        )
    
    # Проверяем, не в черном списке ли токен
    # Check if token is blacklisted
    if auth.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен (отсутствует sub)"
        )
    
    try:
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        print(f"[DEBUG] Найден пользователь: ID={user.id}, Email={user.email}")
        return user
    except ValueError as e:
        print(f"[DEBUG] Ошибка преобразования user_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен (неверный user_id)"
        )

# Обновление данных пользователя
# Update user data
@router.put("/user/update", response_model=schemas.MessageResponse)
def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление данных пользователя"""
    # Update user data
    
    update_data = {}
    
    if user_update.email:
        # Проверяем, не занят ли новый email
        # Check if new email is taken
        existing_user = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже используется"
            )
        update_data["email"] = user_update.email
    
    if user_update.password:
        update_data["hashed_password"] = auth.get_password_hash(user_update.password)
    
    if update_data:
        for key, value in update_data.items():
            setattr(current_user, key, value)
        db.commit()
    
    return {"message": "Данные пользователя обновлены"}

# Просмотр истории входов
# View login history
@router.get("/user/history", response_model=list[schemas.LoginHistoryResponse])
def get_login_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории входов пользователя"""
    # Get user login history
    
    history = db.query(models.LoginHistory).filter(
        models.LoginHistory.user_id == current_user.id
    ).order_by(models.LoginHistory.login_time.desc()).all()
    
    return history

# Выход из системы
# Logout
@router.post("/logout", response_model=schemas.MessageResponse)
def logout(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Выход из системы"""
    # Logout
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    # Извлекаем токен из заголовка Authorization
    # Extract token from Authorization header
    try:
        token = authorization.split("Bearer ")[1]
    except (IndexError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена"
        )
    
    # Проверяем токен
    # Verify token
    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    
    # Добавляем токен в черный список
    # Add token to blacklist
    # Access токен живет 30 минут, добавляем в черный список на 31 минуту для надежности
    # Access token lives for 30 minutes, add to blacklist for 31 minutes for safety
    auth.add_to_blacklist(token, 31 * 60)
    
    return {"message": "Успешный выход из системы"}