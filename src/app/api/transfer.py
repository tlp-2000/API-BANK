from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from app.api.dependencies import get_current_user
from schemas.transfer import TransferCreate, TransferRead
from crud.transfer import crud_transfer
from crud.account import crud_account
from models.transfer import Transfer

router = APIRouter(prefix="/transfers",tags=["transfers"])

@router.post("/",response_model=TransferRead,status_code=201)
async def create__transfer(
    transfer_in : TransferCreate,
    db : AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    # Conta de origem = conta do usuário atual
    from_account = await crud_account.get_all_by_user(db,current_user.id)

     
    if not from_account:
        raise HTTPException(status_code=404, detail="USUARIO NAO POSSUI CONTA")
    
    #assumimos que a conta default do usuário é a primeira
    from_account_id = from_account[0].id

    try:
        transfer = await crud_transfer.create(
            db = db,
            from_account_id=from_account_id, # type: ignore
            to_account_id=transfer_in.to_account_id,
            amount = transfer_in.amount,
            description=transfer_in.description
        )

    except ValueError as e:
        raise HTTPException(404,str(e))
    
    return transfer

@router.get("/",response_model=list[TransferRead],status_code=200)
async def get_transfers(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    # Pegar todas as contas do usuário
    accounts = await crud_account.get_all_by_user(db, current_user.id)
    account_ids = [acc.id for acc in accounts]

    # Buscar transferências onde o usuário participou
    transfers_received = await db.execute(
        select(Transfer).where(Transfer.to_account_id.in_(account_ids))
    )

    transfers_sent = await db.execute(
        select(Transfer).where(Transfer.from_account_id.in_(account_ids))
    )

    all_transfers = transfers_sent.scalars().all() + transfers_received.scalars().all() # type: ignore

    return all_transfers