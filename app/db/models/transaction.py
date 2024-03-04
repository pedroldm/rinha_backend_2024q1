from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    value = Column(Float)
    type = Column(String)
    description = Column(String(10))
    date = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="transactions")