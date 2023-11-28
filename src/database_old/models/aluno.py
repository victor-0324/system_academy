from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime, JSON
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from src.database import Base

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import Base
  

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    idade = Column(String(80), nullable=False)
    sexo = Column(String(80), nullable=False)
    peso = Column(String(80), nullable=False)
    ombro_d = Column(String(80), nullable=False)
    ombro_e = Column(String(80), nullable=False)
    torax = Column(String(80), nullable=False)
    braco_d = Column(String(80), nullable=False)
    braco_e = Column(String(80), nullable=False)
    ant_d = Column(String(80), nullable=False)
    ant_e = Column(String(80), nullable=False)
    cintura = Column(String(80), nullable=False)
    abdome = Column(String(80), nullable=False)
    quadril = Column(String(80), nullable=False)
    coxa_d = Column(String(80), nullable=False)
    coxa_e = Column(String(80), nullable=False)
    pant_d = Column(String(80), nullable=False)
    pant_e = Column(String(80), nullable=False)
    observacao = Column(String(80), nullable=False)
    telefone = Column(String(80), nullable=False)
    login = Column(String(80), nullable=False)
    senha = Column(String(256), nullable=False)
    data_entrada = Column(DateTime, nullable=True)
    data_pagamento = Column(DateTime, nullable=True)
    jatreino = Column(String(100), nullable=False)
    permissao = Column(String(80), nullable=False)
    historico_medidas_peso = Column(JSON, nullable=True) 
    data_atualizacao = Column(DateTime) 