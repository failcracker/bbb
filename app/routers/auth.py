from fastapi import APIRouter, HTTPException, status
from app.models.user import UserLogin
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login")
def login(user_login: UserLogin):
    result = AuthService.login(user_login)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return result
