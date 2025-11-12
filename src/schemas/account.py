from typing import Annotated
from pydantic import BaseModel, Field
from decimal import Decimal

class AccountBase(BaseModel):
    currency : Annotated[str,Field(description="Codigo Da Moeda (ex:BRL)",min_length=3, max_length=5)]



class AccountCreate(AccountBase):
    initial_deposit : Annotated[
        Decimal, 
        Field(description="DEPOSITO INICAIL",examples=['100.00'],ge=0)
    ]

class AccountRead(BaseModel):
    id : int
    owner_id : int
    balance : Decimal
    currency : str


    model_config = {"from_attributes":True}
    