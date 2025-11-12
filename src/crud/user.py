from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from app.core.security import hash_password

class CRUDUser:
 
    @staticmethod
    async def get_by_email(db:AsyncSession, email:str):
          result = await db.execute(select(User).where(User.email == email))
          return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, email: str, password: str) -> User:
            hashed = hash_password(password)
            user = User(email=email, hashed_password=hashed)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

crud_user = CRUDUser()
