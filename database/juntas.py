from sqlalchemy import func
import pandas as pd

from database.connect import SessionLocal
from database.models import Junta


def excluir_juntas_projeto(projeto_id):

    db = SessionLocal()

    try:

        db.query(Junta).filter(
            Junta.projeto_id == projeto_id
        ).delete()

        db.commit()

    finally:

        db.close()


def inserir_junta(junta):

    db = SessionLocal()

    try:

        db.add(junta)
        db.commit()

    finally:

        db.close()


def contar_juntas_projeto(projeto_id):

    db = SessionLocal()

    try:

        return (
            db.query(func.count(Junta.id))
            .filter(
                Junta.projeto_id == projeto_id
            )
            .scalar()
        ) or 0

    finally:

        db.close()


def listar_juntas_projeto(projeto_id):

    db = SessionLocal()

    try:

        return (
            db.query(Junta)
            .filter(
                Junta.projeto_id == projeto_id
            )
            .all()
        )

    finally:

        db.close()


def limpar_valor(valor):

    if pd.isna(valor):
        return None

    texto = str(valor).strip()

    if texto == "":
        return None

    if texto.lower() == "nan":
        return None

    return texto


def limpar_data(valor):

    if pd.isna(valor):
        return None

    return valor


def limpar_inteiro(valor):

    if pd.isna(valor):
        return 0

    try:
        return int(float(valor))
    except:
        return 0


def calcular_status(row):

    soldador = limpar_valor(
        row.get("SOLDADOR RAIZ")
    )

    if soldador:
        return "Soldada"

    return "Pendente"


def importar_dataframe_juntas(df, projeto_id):

    db = SessionLocal()

    try:

        for _, row in df.iterrows():

            junta = Junta(

                projeto_id=projeto_id,

                numero_junta=limpar_valor(
                    row.get("Nº DA JUNTA")
                ),

                desenho_montagem=limpar_valor(
                    row.get("DESENHO DE MONTAGEM")
                ),

                sigla=limpar_valor(
                    row.get("SIGLA")
                ),

                identificacao=limpar_valor(
                    row.get("IDENTIFICAÇÃO")
                ),

                tipo_junta=limpar_valor(
                    row.get("TIPO DE JUNTA")
                ),

                eps=limpar_valor(
                    row.get("EPS")
                ),

                material_1=limpar_valor(
                    row.get("ESPECIFICAÇÃO MATERIAL 1")
                ),

                diametro_1=None,

                espessura_1=None,

                soldador_raiz=limpar_valor(
                    row.get("SOLDADOR RAIZ")
                ),

                soldador_acabamento=limpar_valor(
                    row.get("SOLDADOR ENCHIMENTO  ACABAM")
                ),

                data_solda=limpar_data(
                    row.get("DATA")
                ),

                evs_relatorio=limpar_valor(
                    row.get("RELATÓRIO EVS")
                ),

                evs_real=limpar_inteiro(
                    row.get("EVS_ REAL.")
                ),

                evs_pend=limpar_inteiro(
                    row.get("EVS_PEND")
                ),

                lp_relatorio=limpar_valor(
                    row.get("RELATÓRIO LP")
                ),

                lp_real=limpar_inteiro(
                    row.get("LP_ REAL.")
                ),

                lp_pend=limpar_inteiro(
                    row.get("LP_PEND.")
                ),

                us_relatorio=limpar_valor(
                    row.get("RELATÓRIO US")
                ),

                us_real=limpar_inteiro(
                    row.get("US-REAL.")
                ),

                us_pend=limpar_inteiro(
                    row.get("US_PEND.")
                ),

                observacoes=limpar_valor(
                    row.get("OBSERVAÇÕES")
                ),

                status=calcular_status(row)
            )

            db.add(junta)

        db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()