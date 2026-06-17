from database.connect import SessionLocal
from database.models import Projeto


def listar_projetos():
    db = SessionLocal()

    try:
        return db.query(Projeto).order_by(Projeto.nome).all()

    finally:
        db.close()


def criar_projeto(
    codigo,
    nome,
    cliente,
    local
):
    db = SessionLocal()

    try:

        projeto = Projeto(
            codigo=codigo,
            nome=nome,
            cliente=cliente,
            local=local
        )

        db.add(projeto)
        db.commit()

        return True

    except Exception as e:

        db.rollback()
        raise e

    finally:
        db.close()