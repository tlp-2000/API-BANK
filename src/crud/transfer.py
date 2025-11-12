from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from models.transfer import Transfer
from models.account import Account
from crud.transaction import crud_transaction

class CRUDTransfer:
    @staticmethod
    async def create(db:AsyncSession,from_account_id:int, to_account_id:int,amount:Decimal ,description :str | None = None) -> Transfer:
        if from_account_id == to_account_id:
            raise ValueError("AS CONTAS DEVE SER DIFERENTE")
        
        result = await db.execute(select(Account).where(Account.id == from_account_id)) # type: ignore
        from_account = result.scalar_one_or_none()


        result1 = await db.execute(select(Account).where(Account.id == to_account_id))
        to_account = result1.scalar_one_or_none()


        if not from_account or not to_account:
            raise ValueError("A CONTA DE ORIGEM OU DE DESTIONO NAO FOI ENCONTRADO")
        
        #Verifcando Saldo
        if from_account.balance < amount: # type: ignore
            raise ValueError("SALDO Insuficiente")
        
        #debito e credito
        from_account.balance -= amount # type: ignore
        to_account.balance += amount # type: ignore

        
        #Registrado AS Transferencias
        transfer = Transfer(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount
        )
        db.add(transfer)

        #REGISTRADO TRANSFERENCIAS INDIVIDUAS
        await crud_transaction.create(
            db=db,
            account_id=from_account_id,
            amount=amount,
            type="debit",
            description=description or "TRANSFERENCIA ENVIADA")
        
        await crud_transaction.create(
            db=db,
            account_id=to_account_id,
            amount=amount,
            type="credit",
            description=description or "TRANSFERENCIA RECEBIDA"
        )

        await db.commit()
        await db.refresh(transfer)

        return transfer
    


crud_transfer = CRUDTransfer()

