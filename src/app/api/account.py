from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from schemas.account import AccountCreate, AccountRead
from crud.account import crud_account
from app.api.dependencies import get_current_user 

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountRead,status_code=201)
async def create_account(
    account_in: AccountCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    account = await crud_account.create(
        db,
        owner_id=current_user.id,
        initial_deposit=account_in.initial_deposit,
        currency=account_in.currency
    )
    return account


@router.get("/", response_model=list[AccountRead])
async def get_my_accounts(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    accounts = await crud_account.get_all_by_user(db, current_user.id)
    return accounts
    