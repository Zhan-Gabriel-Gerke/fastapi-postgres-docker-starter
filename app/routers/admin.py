from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from .auth import get_current_admin_user
from ..database import get_db
from ..models import Todos

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_admin_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(_: user_dependency, db: db_dependency):
    result = await db.execute(select(Todos))
    return result.scalars().all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(_: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    result = await db.execute(select(Todos).filter(Todos.id == todo_id))
    todo_model = result.scalars().first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    await db.delete(todo_model)
    await db.commit()