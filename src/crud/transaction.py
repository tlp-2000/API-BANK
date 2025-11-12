from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from models.transaction import Transaction
from models.account import Account

class CRUDTransaction:
    @staticmethod
    async def create(db:AsyncSession,account_id: int, amount:Decimal, type: str, description : str | None= None):
        # 1. Buscar conta
        result = await db.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()

        if not account:
            raise ValueError("Conta Nao Encontrada")
        
        #2. VALIDA TIPO
        if type not in ("credit","debit"):
            raise ValueError("tipo invalido use somente (credit,debit)")
        
        #3 = Operaçao e atualizaçao do saldo
        if type == "credit":
            account.balance = account.balance + amount  # type: ignore

        elif type == "debit":
            if account.balance < amount: # pyright: ignore[reportGeneralTypeIssues]
                raise ValueError("Saldo insuficiente.")
            account.balance = account.balance - amount # type: ignore

        #4 = criar transaçao realizada
        transaction = Transaction(
            account_id = account_id,
            amount = amount,
            type = type,
            description = description,
        )

        db.add(transaction)
        await db.commit()

        #5 = Atualizar os dois objetos
        await db.refresh(account)
        await db.refresh(transaction)

        return transaction


    @staticmethod
    async def get_all_by_account(db: AsyncSession, account_id: int):
        result = await db.execute(
            select(Transaction).where(Transaction.account_id == account_id) 
        )
        return result.scalars().all()


crud_transaction = CRUDTransaction()
