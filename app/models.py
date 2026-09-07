from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from datetime import datetime

from .database import Base

class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)

    cliente = Column(String(100), nullable=False)

    servico = Column(String(200), nullable=False)

    cidade = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    data_agendada = Column(Date, nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="ABERTO"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )