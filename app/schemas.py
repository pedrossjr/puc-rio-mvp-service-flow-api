from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

class ChamadoBase(BaseModel):
    cliente: str
    servico: str
    cidade: str
    latitude: float
    longitude: float
    data_agendada: date

class ChamadoCreate(ChamadoBase):
    pass

class ChamadoUpdate(BaseModel):
    cliente: str | None = None
    servico: str | None = None
    cidade: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    data_agendada: date | None = None
    status: str | None = None

class ChamadoResponse(ChamadoBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)