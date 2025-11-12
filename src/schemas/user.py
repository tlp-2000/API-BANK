from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


# -------------------------------------------------------------------
# Schema para criação de usuário (cadastro)
# -------------------------------------------------------------------
class UserCreate(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            description="Email do usuário",
            examples=["thipaulino@gmail.com"],
            max_length=50,
        ),
    ]
    password: Annotated[
        str,
        Field(
            description="Senha do usuário",
            examples=["12354"],
            min_length=6,
        ),
    ]


# -------------------------------------------------------------------
# Schema para login
# -------------------------------------------------------------------
class UserLogin(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            description="Email do usuário",
            examples=["user@example.com"],
            max_length=50,
        ),
    ]
    password: Annotated[
        str,
        Field(
            description="Senha do usuário",
            examples=["12@tl4"],
            min_length=6,
        ),
    ]


# -------------------------------------------------------------------
# Schema de leitura (resposta da API)
# -------------------------------------------------------------------
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}


# -------------------------------------------------------------------
# Schema do token JWT retornado no login
# -------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
