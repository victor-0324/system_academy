from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from src.database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    idade = Column(String(80), nullable=False)
    sexo = Column(String(80), nullable=False)
    altura = Column(String(80), nullable=False)
    peso = Column(String(80), nullable=False)
    ombro = Column(String(80), nullable=False)
    torax = Column(String(80), nullable=False)
    braco = Column(String(80), nullable=False)
    ant = Column(String(80), nullable=False)
    cintura = Column(String(80), nullable=False)
    abdome = Column(String(80), nullable=False)
    quadril = Column(String(80), nullable=False)
    coxa = Column(String(80), nullable=False)
    pant = Column(String(80), nullable=False)
    observacao = Column(String(80), nullable=False)
    telefone = Column(String(80), nullable=False)
    login = Column(String(80), nullable=False)
    senha = Column(String(256), nullable=False)
    data_entrada = Column(DateTime, nullable=True)
    data_pagamento = Column(DateTime, nullable=True)
    jatreino = Column(String(100), nullable=False)
    permissao = Column(String(80), nullable=False)

    def set_password(self, password):
        self.senha = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def is_active(self):
        # Aqui você pode implementar a lógica para verificar se o aluno está ativo
        return True 
    # Adicionando métodos necessários para Flask-Login
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True  # ou implemente a lógica desejada

    def is_anonymous(self):
        return False

    # Relacionamento com a tabela ExerciciosAluno
    exercicios = relationship('ExerciciosAluno', back_populates='aluno')

    def __repr__(self):
        return (
        f"{self.id} {self.nome} {self.idade} {self.sexo} {self.altura} {self.peso} "
        f"{self.ombro} {self.torax} {self.braco} {self.ant} {self.cintura} {self.abdome} "
        f"{self.quadril} {self.coxa} {self.pant} {self.observacao} {self.telefone} "
        f"{self.login} {self.senha} {self.data_entrada} {self.data_pagamento} {self.jatreino} {self.permissao}"
         )
class ExerciciosAluno(Base):
    __tablename__ = "exercicios_aluno"
    id = Column(Integer, primary_key=True)
    tipoTreino = Column(String(80), nullable=False)
    exercicio = Column(String(80), nullable=False)
    serie = Column(String(80), nullable=False)
    repeticao = Column(String(80), nullable=False)
    descanso = Column(String(80), nullable=False)
    carga = Column(String(80), nullable=False)
    
    # Chave estrangeira referenciando a tabela Aluno
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    
    # Relacionamento com a tabela Aluno
    aluno = relationship('Aluno', back_populates='exercicios')

    def __repr__(self):
        return f"{self.tipoTreino} {self.exercicio} {self.serie} {self.repeticao} {self.descanso} {self.carga}"
 