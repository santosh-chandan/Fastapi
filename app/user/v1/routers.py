from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.engine_psgl import get_db
from typing import List
from app.user.services import userService
from app.user.schema import CreateUser, GetUser, UpdateUser

router = APIRouter(prefix='/v1/user')

# Get Users
@router.get('/', response_model=List[GetUser])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    return await userService.get_users(db)

# Get User BY Id
@router.get('/{id}', response_model=GetUser)
async def get_user_by_id(
    id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await userService.get_user_by_id(id, db)

# Create User API
@router.post('/', response_model=GetUser)
async def create_user(
    data: CreateUser, 
    db = Depends(get_db)
):
    return await userService.create_user(data, db)

# Update User
@router.patch('/update/{id}', response_model=GetUser)
async def update_user(
    id: int, 
    data:UpdateUser,
    db: AsyncSession=Depends(get_db)
):
    return await userService.update_user(id, data, db)

# Delete User
@router.delete('/delete/{id}', status_code=204)
async def delete_user(id: int, db: AsyncSession=Depends(get_db)):
    await userService.delete_user(id, db)
    return Response(status_code=204)
