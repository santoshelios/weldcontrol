from database.connect import SessionLocal
from database.models import Junta

from sqlalchemy import func


def obter_kpis_projeto(projeto_id):

    db = SessionLocal()

    try:

        total = (
            db.query(func.count(Junta.id))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        soldadas = (
            db.query(func.count(Junta.id))
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.soldador_raiz.isnot(None)
            )
            .scalar()
        ) or 0

        evs = (
            db.query(func.count(Junta.id))
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.evs_real.isnot(None)
            )
            .scalar()
        ) or 0

        lp = (
            db.query(func.count(Junta.id))
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.lp_real.isnot(None)
            )
            .scalar()
        ) or 0

        us = (
            db.query(func.count(Junta.id))
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.us_real.isnot(None)
            )
            .scalar()
        ) or 0

        pendentes = total - soldadas

        percentual = (
            round((soldadas / total) * 100, 1)
            if total > 0
            else 0
        )

        return {
            "total": total,
            "soldadas": soldadas,
            "evs": evs,
            "lp": lp,
            "us": us,
            "pendentes": pendentes,
            "percentual": percentual
        }

    finally:

        db.close()

def obter_tipo_junta(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.tipo_junta,
                func.count(Junta.id)
            )
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.tipo_junta.isnot(None),
                Junta.tipo_junta != ""
            )
            .group_by(
                Junta.tipo_junta
            )
            .order_by(
                func.count(Junta.id).desc()
            )
            .all()
        )

        return dados

    finally:

        db.close()


def obter_fluido(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.sigla,
                func.count(Junta.id)
            )
            .filter(
                Junta.projeto_id == projeto_id
            )
            .group_by(
                Junta.sigla
            )
            .all()
        )

        return dados

    finally:

        db.close()

def obter_top_soldadores(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.soldador_raiz,
                func.count(Junta.id)
            )
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.soldador_raiz.isnot(None)
            )
            .group_by(
                Junta.soldador_raiz
            )
            .order_by(
                func.count(Junta.id).desc()
            )
            .limit(10)
            .all()
        )

        return dados

    finally:

        db.close()


def obter_top_isometricos(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.desenho_montagem,
                func.count(Junta.id)
            )
            .filter(
                Junta.projeto_id == projeto_id
            )
            .group_by(
                Junta.desenho_montagem
            )
            .order_by(
                func.count(Junta.id).desc()
            )
            .limit(10)
            .all()
        )

        return dados

    finally:

        db.close()

def obter_tabela_fluido(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.sigla,
                func.count(Junta.id)
            )
            .filter(
                Junta.projeto_id == projeto_id
            )
            .group_by(
                Junta.sigla
            )
            .order_by(
                func.count(Junta.id).desc()
            )
            .all()
        )

        return dados

    finally:

        db.close()

def obter_tabela_analitica(projeto_id):

    db = SessionLocal()

    try:

        dados = (
            db.query(
                Junta.sigla,
                func.count(Junta.id).label("total"),
                func.count(Junta.soldador_raiz).label("soldadas")
            )
            .filter(
                Junta.projeto_id == projeto_id
            )
            .group_by(
                Junta.sigla
            )
            .order_by(
                func.count(Junta.id).desc()
            )
            .all()
        )

        resultado = []

        for sigla, total, soldadas in dados:

            pendentes = total - soldadas

            percentual = (
                round((soldadas / total) * 100, 1)
                if total > 0
                else 0
            )

            resultado.append({
                "Fluido": sigla,
                "Qtde_Juntas": total,
                "Soldadas": soldadas,
                "Pendentes": pendentes,
                "Avanço_%": percentual
            })

        return resultado

    finally:

        db.close()