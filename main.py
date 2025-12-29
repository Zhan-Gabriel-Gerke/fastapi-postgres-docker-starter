from fastapi import FastAPI, Depends, HTTPException, status
from app.database import engine, get_db
from app.models import Base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import auth, todos, admin, users
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthy", status_code=status.HTTP_200_OK)
async def get_healthy(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed"
            )

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
