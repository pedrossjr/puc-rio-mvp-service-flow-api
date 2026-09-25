from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud
from .database import Base, engine, get_db
from .schemas import (
    ChamadoCreate,
    ChamadoResponse,
    ChamadoUpdate
)

from .services.risk_service import RiskAPIIndisponivel, calcular_risco

from .services.weather_service import OpenMeteoIndisponivel, consultar_clima

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ServiceFlow API",
    description="API principal para gerenciamento de atendimentos técnicos.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "aplicacao": "ServiceFlow API",
        "status": "online"
    }

@app.get(
    "/chamados",
    response_model=list[ChamadoResponse]
)
def listar_chamados(
    db: Session = Depends(get_db)
):
    return crud.listar_chamados(db)

@app.get(
    "/chamados/{chamado_id}",
    response_model=ChamadoResponse
)
def buscar_chamado(
    chamado_id: int,
    db: Session = Depends(get_db)
):
    chamado = crud.buscar_chamado(
        db,
        chamado_id
    )

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado."
        )

    return chamado

@app.post(
    "/chamados",
    response_model=ChamadoResponse,
    status_code=201
)
def criar_chamado(
    chamado: ChamadoCreate,
    db: Session = Depends(get_db)
):
    return crud.criar_chamado(
        db,
        chamado
    )

@app.put(
    "/chamados/{chamado_id}",
    response_model=ChamadoResponse
)
def atualizar_chamado(
    chamado_id: int,
    dados: ChamadoUpdate,
    db: Session = Depends(get_db)
):
    chamado = crud.buscar_chamado(
        db,
        chamado_id
    )

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado."
        )

    return crud.atualizar_chamado(
        db,
        chamado,
        dados
    )

@app.delete(
    "/chamados/{chamado_id}",
    status_code=204
)
def excluir_chamado(
    chamado_id: int,
    db: Session = Depends(get_db)
):
    chamado = crud.buscar_chamado(
        db,
        chamado_id
    )

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado."
        )

    crud.excluir_chamado(
        db,
        chamado
    )

@app.get("/chamados/{chamado_id}/risco")
def consultar_risco(chamado_id: int, db: Session = Depends(get_db)):
    chamado = crud.buscar_chamado(db, chamado_id)

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado."
        )

    try:
        clima = consultar_clima(
            latitude=chamado.latitude,
            longitude=chamado.longitude
        )
    except OpenMeteoIndisponivel:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível consultar os dados meteorológicos."
        )

    try:
        resultado = calcular_risco(
            temperatura=clima["temperatura"],
            chuva=clima["chuva"],
            vento=clima["vento"]
        )
    except RiskAPIIndisponivel:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível consultar o risco climático."
        )

    return {
        "chamado": chamado.id,
        "cliente": chamado.cliente,
        "servico": chamado.servico,
        "cidade": chamado.cidade,
        "clima": clima,
        "risco": resultado
    }