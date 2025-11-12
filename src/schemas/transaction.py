from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
from decimal import Decimal

class TransactionBase(BaseModel):
    amount : Annotated[Decimal, Field(description="VALOR DA TRANSAÇAO",examples=["150.00"])]
    type : Annotated[str,Field(description="TIPO DA TRANSAÇAO(credit OU debit)",examples=["credit"])]
    description: Annotated[str | None, Field(description="Descrição opcional", examples=["Depósito inicial"])] = None


class TransactionCreate(TransactionBase):
    pass


#reponse model
class TransactionRead(BaseModel):
    id: Annotated[int,Field(description="ID TRANSAÇAO",examples=['1'])]
    account_id: Annotated[int,Field(description="ID CONTA")]
    amount: Annotated[Decimal,Field(description="VALOR TRANSAÇAO",examples=['150.00'])]
    type: Annotated[str,Field(description="TIPO DA TRANSAÇAO(DEBITO OU CREDITO)",examples=['Credito'])]
    description: Annotated[str | None, Field(description="Descrição", examples=["Transferência"])]
    created_at: Annotated[datetime, Field(description="Data e hora")]

    model_config = {"from_attributes":True}