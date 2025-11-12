from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.account import Account


class CRUDAccount:

    @staticmethod
    async def create(db: AsyncSession,owner_id: int,initial_deposit: Decimal,currency: str = "BRL"):
        account = Account(
            owner_id=owner_id,
            balance=initial_deposit,
            currency=currency
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account

    
    @staticmethod
    async def get_by_id(db:AsyncSession, account_id: int):
        result = await db.execute(select(Account).where(Account.id == account_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_by_user(db:AsyncSession, user_id: int):
        result = await db.execute(select(Account).where(Account.owner_id == user_id))
        return result.scalars().all()


crud_account = CRUDAccount()
