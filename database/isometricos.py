from database.connect import SessionLocal
from database.models import Isometrico


def listar_isometricos():

    db = SessionLocal()

    try:

        return (
            db.query(Isometrico)
            .order_by(
                Isometrico.desenho,
                Isometrico.revisao.desc()
            )
            .all()
        )

    finally:
        db.close()


def criar_isometrico(isometrico):

    db = SessionLocal()

    try:

        db.add(isometrico)

        db.commit()

        db.refresh(isometrico)

        return isometrico

    finally:

        db.close()

from database.models import Isometrico


def salvar_isometrico(
    projeto_id,
    desenho,
    revisao,
    data_emissao,
    sistema,
    area,
    qtd_spools,
    qtd_juntas,
    status
):

    db = SessionLocal()

    try:

        novo = Isometrico(
            projeto_id=projeto_id,
            desenho=desenho.upper(),
            revisao=revisao,
            data_emissao=data_emissao,
            sistema=sistema,
            area=area,
            qtd_spools=qtd_spools,
            qtd_juntas=qtd_juntas,
            status=status,
            ativo=True
        )
        print("SALVANDO ISOMETRICO")
        db.add(novo)

        db.commit()

        db.refresh(novo)

        return novo

    finally:

        db.close()