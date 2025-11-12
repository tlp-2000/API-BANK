from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer,primary_key = True, index=True)

    #DONO DA CONTA (FK PARA USUARIOS)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False)

    #SALDO COM Decimal 
    balance = Column(Numeric(10,2), nullable=False, default=0)

    currency = Column(String,default="BRL",nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now())

    owner = relationship("User",backref= "accounts")