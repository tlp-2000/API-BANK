from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)

    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos com contas
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])
