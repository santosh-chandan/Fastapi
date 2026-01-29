from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import hash_password
from app.user.models import User
from app.core.exceptions.exceptions import (
    UserNotFound, 
    UserAlreadyExist
)

# Repository or Service Class never knows about FastAPI or schemas
# Service raises domain exceptions.
# Router returns data only.
# FastAPI maps domain exceptions → HTTP responses globally.
# Router should NOT know about business rules.
# No try, No except, No HTTPException - This feels scary at first — but it’s the right design.


# User Service Class
class UserService():
    # Get USers
    async def get_users(self, db: AsyncSession):
        result = await db.execute(
            select(User)
        )
        return result.scalars().all()


    # Get User By Id
    async def get_user_by_id(self, id: int, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.id == id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound("User not found")
        return user


    # Get user by email
    async def get_by_email(self, email: str, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()


    # Create User
    async def create_user(self, data, db: AsyncSession):
        existing = await self.get_by_email(data.email,db)
        if existing:
            raise UserAlreadyExist("Email Already Exist.")
       
        user = User(
            name= data.name, 
            email= data.email,
            password= hash_password(data.password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


    # Update User
    async def update_user(self, id: int, data, db: AsyncSession):
        result = await db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound("User not found")
        
        if data.email and user.email != data.email:
            existing = await self.get_by_email(data.email,db)
            if existing:
                raise UserAlreadyExist("User already exist")
        
        # data is a Pydantic model:
        # model_dump(exclude_unset=True) - remove those fields which dont have value or None. exclude - remove, unset - No value.
        # for field, value in {...}.items(): - dict iteration
        # setattr - It exactly the same as writing: user.name = "Santosh Updated" for all fields But dynamic. No need to manual set.
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "password":
                value = hash_password(value)
            setattr(user, field, value)
        # As user is sqlalchemy object and is already in db session so no need to do db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
    

    # Delete User
    async def delete_user(self, id: int, db: AsyncSession):
        result = await db.execute(
            select(User).where(User.id == id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound("User not exist")

        await db.delete(user)
        await db.commit()


userService = UserService()
