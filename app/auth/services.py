# app/auth/services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Header
from datetime import timedelta
from app.core.exceptions.exceptions import UserNotFound, InvalidCredentials
from app.core.security import create_token, verify_password, decode_token, ACCESS_TOKEN_MINUTES, REFRESH_TOKEN_DAYS
from app.user.models import User

class AuthService():

    # Do login
    async def login(self, data, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()
        if not user or verify_password(data.password, user.password):
            raise InvalidCredentials("Invalid email or password")
        
        access_token = create_token(
            {"sub": str(user.id)},
            expres_delta = timedelta(minutes=ACCESS_TOKEN_MINUTES),
            token_type = 'access'
            )
        
        refresh_token = create_token(
            {"sub": str(user.id)},
            expres_delta= timedelta(days=REFRESH_TOKEN_DAYS),
            token_type= 'refresh'
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
     
    # Get current user
    async def get_current_user(self, db: AsyncSession, authorization: str = Header(...)):
        token = self._extract_token(authorization)

        # Decode JWT (checks exp automatically)
        payload = decode_token(token)
        if payload.get('type') != 'access':
            raise InvalidCredentials("Access token required.")
        
        user_id = payload.get("sub")
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotFound("User not found")

        return user

    def _extract_token(self, autherization: str) -> str:
        if not autherization.startswith("Bearer "):
            raise InvalidCredentials(" Invalid Credentials")
        
        return autherization.split(" ")[1]
   
    # Refresh token
    async def refresh_token(self, authorization: str):
        token = self._extract_token(authorization)
        payload = decode_token(token)

        if payload.type != 'refresh':
            raise InvalidCredentials("Refresh token required.")
        
        new_access_token = create_token(
            {"sub": payload['sub']},
            timedelta(minutes= ACCESS_TOKEN_MINUTES),
            'access'
        )

        return {
            'access_token': new_access_token,
            'token_type': 'bearer'
        }


authService = AuthService()
