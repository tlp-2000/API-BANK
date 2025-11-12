from typing import Annotated
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class TransferCreate(BaseModel):
    to_account_id: Annotated[int, Field(description="Conta que vai receber", examples=[2])]
    amount: Annotated[Decimal, Field(description="VALOR DA TRANSFERENCIA",examples=["100.00"])]
    description: Annotated[str | None, Field(description="Descrição opcional", examples=["PAGAMENTO"])] = None


class TransferRead(BaseModel):
    id: Annotated[int, Field(description="IDENTIFICADOR",examples=[1])]
    from_account_id: Annotated[int, Field(description="CONTA DE ORIGEM",examples=[2])]
    to_account_id: Annotated[int, Field(description="CONTA QUE VAI RECEBER",examples=[2])]
    amount: Annotated[Decimal,Field(description="VALOR DA TRANSFERENCIAS",examples=['100.00'])]
    created_at: Annotated[datetime, Field(description="DATA E HORA DA TRANSEFERENCIA")]

    model_config = {"from_attributes": True}
