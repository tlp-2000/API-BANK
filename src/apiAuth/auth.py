from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserRead, Token,UserLogin
from db.session import get_async_session
from crud.user import crud_user
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in:UserCreate, db:AsyncSession = Depends(get_async_session)):
    #VERIFICANDO A DUPLICIDADE DO EMAIL
    existing = await crud_user.get_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400,detail="EMAIL JA EXISTANTE")
    #SE O USUARIO NAO EXISTIR,CRIA O USUARIO
    user = await crud_user.create(db, email = user_in.email , password=user_in.password)
    return user


@router.post("/login",response_model=Token)
async def login(user_in:UserLogin, db: AsyncSession = Depends(get_async_session)):
    user = await crud_user.get_by_email(db, user_in.email)
    
    if not user or not verify_password(user_in.password, user.hashed_password): # pyright: ignore[reportArgumentType]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    token = create_access_token(subject=str(user.id))
    
    return {"access_token": token, "token_type": "bearer"}


