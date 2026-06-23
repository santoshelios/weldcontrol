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

        evs_real = (
            db.query(func.sum(Junta.evs_real))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        evs_pend = (
            db.query(func.sum(Junta.evs_pend))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        lp_real = (
            db.query(func.sum(Junta.lp_real))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        lp_pend = (
            db.query(func.sum(Junta.lp_pend))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        us_real = (
            db.query(func.sum(Junta.us_real))
            .filter(Junta.projeto_id == projeto_id)
            .scalar()
        ) or 0

        us_pend = (
            db.query(func.sum(Junta.us_pend))
            .filter(Junta.projeto_id == projeto_id)
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
            "pendentes": pendentes,
            "percentual": percentual,

            "evs_real": evs_real,
            "evs_pend": evs_pend,

            "lp_real": lp_real,
            "lp_pend": lp_pend,

            "us_real": us_real,
            "us_pend": us_pend
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
                Junta.sigla.label("fluido"),

                func.count(Junta.id).label("total"),

                func.count(Junta.soldador_raiz).label("soldadas"),

                func.sum(Junta.evs_real).label("evs_real"),
                func.sum(Junta.evs_pend).label("evs_pend"),

                func.sum(Junta.lp_real).label("lp_real"),
                func.sum(Junta.lp_pend).label("lp_pend"),

                func.sum(Junta.us_real).label("us_real"),
                func.sum(Junta.us_pend).label("us_pend")
            )
            .filter(
                Junta.projeto_id == projeto_id,
                Junta.sigla.isnot(None),
                Junta.sigla != ""
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

        for (
            fluido,
            total,
            soldadas,
            evs_real,
            evs_pend,
            lp_real,
            lp_pend,
            us_real,
            us_pend
        ) in dados:

            pendentes = total - soldadas

            percentual = (
                round(
                    (soldadas / total) * 100,
                    1
                )
                if total > 0
                else 0
            )

            resultado.append({

                "Fluido": fluido,

                "Qtde_Juntas": total,

                "EVS_Real": evs_real or 0,
                "EVS_Pend": evs_pend or 0,

                "LP_Real": lp_real or 0,
                "LP_Pend": lp_pend or 0,

                "US_Real": us_real or 0,
                "US_Pend": us_pend or 0,

                "Soldadas": soldadas,
                "Pendentes": pendentes,

                "Avanço_%": percentual
            })

        return resultado

    finally:

        db.close()

def listar_fluidos(projeto_id):

    db = SessionLocal()

    try:

        return [
            r[0]
            for r in (
                db.query(Junta.sigla)
                .filter(
                    Junta.projeto_id == projeto_id,
                    Junta.sigla.isnot(None),
                    Junta.sigla != ""
                )
                .distinct()
                .order_by(Junta.sigla)
                .all()
            )
        ]

    finally:

        db.close()


def listar_tipos_junta(projeto_id):

    db = SessionLocal()

    try:

        return [
            r[0]
            for r in (
                db.query(Junta.tipo_junta)
                .filter(
                    Junta.projeto_id == projeto_id,
                    Junta.tipo_junta.isnot(None),
                    Junta.tipo_junta != ""
                )
                .distinct()
                .order_by(Junta.tipo_junta)
                .all()
            )
        ]

    finally:

        db.close()