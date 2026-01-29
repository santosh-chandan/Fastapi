# app/auth/v1/routers/py
from fastapi import APIRouter, Depends, Header
from app.core.engine_psgl import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schema import CreateLogin, SendToken
from app.user.schema import GetUser
from app.auth.services import authService
from app.user.models import User

router = APIRouter('/v1/auth', tags=['Auth'])


@router.post('/login', response_model= SendToken)
async def login(data: CreateLogin, db:AsyncSession = Depends(get_db)):
    return await authService.login(data, db)

@router.post('/refresh_token', response_model= SendToken)
async def refresh_token(authorization: str = Header(...)):
    return await authService.refresh_token(authorization)

@router.get('/me', response_model= GetUser)
async def get_user(
    current_user: User = Depends(authService.get_current_user), 
    db: AsyncSession = Depends(get_db)
    ):
    return current_user

@router.post('/logout')
async def change_password(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    await authService.logout(authorization, db)
    # Jwt token with expiraton is stateless so it managed by frontend.
    # But just get request and validate access token then send to client to make him self logout
