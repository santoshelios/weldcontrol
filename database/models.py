from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nome = Column(String(200), nullable=False)
    cliente = Column(String(200))
    local = Column(String(200))
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True)
    senha_hash = Column(Text)
    perfil = Column(String(30))
    ativo = Column(Boolean, default=True)


class Soldador(Base):
    __tablename__ = "soldadores"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True)
    nome = Column(String(200))
    qualificacao = Column(String(100))
    validade_qualificacao = Column(Date)
    ativo = Column(Boolean, default=True)


class Junta(Base):
    __tablename__ = "juntas"

    id = Column(Integer, primary_key=True)

    projeto_id = Column(Integer, ForeignKey("projetos.id"))

    numero_junta = Column(String(100))
    desenho_montagem = Column(Text)
    sigla = Column(String(50))
    identificacao = Column(Text)

    tipo_junta = Column(String(50))
    eps = Column(String(100))

    material_1 = Column(String(100))
    diametro_1 = Column(Numeric(10, 2))
    espessura_1 = Column(Numeric(10, 2))

    soldador_raiz = Column(String(50))
    soldador_acabamento = Column(String(50))

    data_solda = Column(Date)

    evs_relatorio = Column(String(100))
    evs_real = Column(Date)

    lp_relatorio = Column(String(100))
    lp_real = Column(Date)

    us_relatorio = Column(String(100))
    us_real = Column(Date)

    fluxoteste = Column(String(100))
    relatorio_th = Column(String(100))

    observacoes = Column(Text)

    status = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)


class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True)

    junta_id = Column(Integer)

    usuario = Column(String(100))
    acao = Column(Text)

    data_hora = Column(DateTime, default=datetime.utcnow)