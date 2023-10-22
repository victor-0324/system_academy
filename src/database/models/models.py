from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Treino(Base):
    __tablename__ = "treinos"
    id = Column(Integer, primary_key=True)
    dia_treino = Column(String(200), nullable=False)
    horario = Column(String(100), nullable=False)
    exercicio_treino = Column(String(200), nullable=False)
    inicio = Column(String(100))
    obejetivo = Column(String(100))
    
    def __repr__(self):
        return f"{self.dia_treino} {self.horario}{self.exercicio} {self.inicio_treino} {self.obejetivo}"

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    treinos = relationship('Treino', backref='aluno', lazy=True)
    # Adicione outras colunas relacionadas a alunos

    def __repr__(self):
        return f"{self.nome} {self.login}{self.senha}{self.treinos}"

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    # Adicione outras colunas relacionadas a administradores

    def __repr__(self):
        return f"{self.nome}{self.senha}{self.login}"
