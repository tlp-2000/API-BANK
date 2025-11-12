from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from db.session import get_async_session
from models.user import User


# Esquema correto para JWT (substitui OAuth2PasswordBearer)
auth_scheme = HTTPBearer()


async def get_current_user(
    credentials = Depends(auth_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Extrai o token Bearer do header Authorization,
    valida o JWT e retorna o usuário autenticado.
    """

    token = credentials.credentials  # extrai o JWT enviado como Bearer Token

    # 1. Decodificar o JWT
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")  # type: ignore # subject do token
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

    # 2. Buscar usuário no banco
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return user
