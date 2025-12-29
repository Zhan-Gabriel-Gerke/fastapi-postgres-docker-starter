from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from .auth import get_current_user
from ..database import get_db
from ..models import Users
from ..schemas import UserVerification, UserVerificationPhone

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    result = await db.execute(select(Users).filter(Users.id == user.get("id")))
    return result.scalars().first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_data: UserVerification):
    result = await db.execute(select(Users).filter(Users.id == user.get("id")))
    user_model = result.scalars().first()

    if not bcrypt_context.verify(user_data.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_data.new_password)
    db.add(user_model)
    await db.commit()

@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_nuber(user: user_dependency, db: db_dependency, user_data: UserVerificationPhone):
    result = await db.execute(select(Users).filter(Users.id == user.get("id")))
    user_model = result.scalars().first()

    if not bcrypt_context.verify(user_data.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect Password")
    user_model.phone_number = user_data.new_phone_number
    db.add(user_model)
    await db.commit()