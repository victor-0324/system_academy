from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Treino(Base):
    __tablename__ = "treinos"
    id = Column(Integer, primary_key=True)
    descricao = Column(String(200), nullable=False)
    

    def __repr__(self):
        return f"Treino: {self.descricao}"

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    treinos = relationship('Treino', backref='aluno', lazy=True)
    # Adicione outras colunas relacionadas a alunos

    def __repr__(self):
        return f"Aluno: {self.nome}"

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    login = Column(String(80), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    # Adicione outras colunas relacionadas a administradores

    def __repr__(self):
        return f"Admin: {self.nome}"
