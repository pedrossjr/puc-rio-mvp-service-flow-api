from sqlalchemy.orm import Session

from .models import Chamado
from .schemas import ChamadoCreate, ChamadoUpdate

def criar_chamado(
    db: Session,
    chamado: ChamadoCreate
):
    novo_chamado = Chamado(
        **chamado.model_dump()
    )

    db.add(novo_chamado)
    db.commit()
    db.refresh(novo_chamado)

    return novo_chamado

def listar_chamados(db: Session):
    return db.query(Chamado).all()

def buscar_chamado(
    db: Session,
    chamado_id: int
):
    return (
        db.query(Chamado)
        .filter(Chamado.id == chamado_id)
        .first()
    )

def atualizar_chamado(
    db: Session,
    chamado: Chamado,
    dados: ChamadoUpdate
):
    dados_atualizacao = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in dados_atualizacao.items():
        setattr(chamado, campo, valor)

    db.commit()
    db.refresh(chamado)

    return chamado

def excluir_chamado(
    db: Session,
    chamado: Chamado
):
    db.delete(chamado)
    db.commit()