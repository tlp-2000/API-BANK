from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True,index=True)

    #FK PARA A CONTA
    account_id = Column(Integer, ForeignKey("accounts.id"),nullable=False)

    #VALOR DA TRANSAÇAO REAL
    amount = Column(Numeric(10,2),nullable = False)

    #tipo da transaçao CREDITO(ENTRADA) E DEBITO(SAIDA)
    type = Column(String, nullable = False)


    #Descriçao da transaçao DEBITO OU CREDITO
    description = Column(String, nullable = True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #RELACIONAMENTO COM ACCOUNT
    account = relationship("Account",backref = "transactions")