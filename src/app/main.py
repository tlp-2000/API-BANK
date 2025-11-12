import asyncio
from fastapi import FastAPI
from apiAuth import auth
from db.session import engine, Base
from app.api import account
from app.api.transaction import router as transaction_router
from app.api.account import router as account_router
from app.api.transfer import router as transfer_router

app = FastAPI(title="Bank API")

app.include_router(auth.router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(transfer_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

