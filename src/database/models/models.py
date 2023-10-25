from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    idade = Column(String(80), nullable=False)
    sexo = Column(String(80), nullable=False)
    altura = Column(String(80), nullable=False)
    peso = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    telefone = Column(String(80), nullable=False)
    dia_semana = Column(String(80), nullable=False)
    login = Column(String(80), nullable=False)
    senha = Column(String(80), nullable=False)

    tipo_treino = Column(String(200), nullable=False)
    horario = Column(String(100), nullable=False)
    inicio = Column(String(100))
    obj = Column(String(100))

    def __repr__(self):
        return f"{self.nome} {self.login} {self.senha} {self.telefone} {self.email} {self.idade} {self.peso} {self.altura} {self.sexo} {self.dia_semana} {self.obj} {self.tipo_treino} {self.horario} {self.inicio}"

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    

    def __repr__(self):
        return f"{self.nome}{self.senha}{self.login}"
