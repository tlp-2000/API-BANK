from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from schemas.transaction import TransactionCreate, TransactionRead
from crud.transaction import crud_transaction
from app.api.dependencies import get_current_user
from crud.account import crud_account


router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/{account_id}",response_model=TransactionRead, status_code=201)
async def create_transaction(account_id:int, transaction_in : TransactionCreate,db:AsyncSession = Depends(get_async_session),current_user = Depends(get_current_user),):
    # 1) Garantir que a conta existe e pertence ao usuário autenticado
    account = await crud_account.get_by_id(db,account_id)
    if not account:
        raise HTTPException(status_code=404,detail="CONTA NAO ENCONTRADA")
    
    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="ACESSO NEGADO A ESTA CONTA")
    
     # 2) Tentar criar transação + atualizar saldo

    try:
        transaction = await crud_transaction.create(
            db = db,
            account_id=account_id,
            amount=transaction_in.amount,
            type = transaction_in.type,
            description=transaction_in.description,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return transaction



@router.get("/{account_id}", response_model=list[TransactionRead])
async def get_transactions(
    account_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    # 1) Garantir que a conta existe e pertence ao usuário autenticado
    account = await crud_account.get_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a esta conta")
    
    transactions = await crud_transaction.get_all_by_account(db,account_id)
    return transactions
