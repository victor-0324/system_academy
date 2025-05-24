from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    func,
    Interval,
)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, timezone
from src.database import Base


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    idade = Column(DateTime, nullable=True)
    sexo = Column(String(30), nullable=False)
    telefone = Column(String(30), nullable=False)
    login = Column(String(30), nullable=False)
    senha = Column(String(50), nullable=False)
    data_entrada = Column(DateTime, nullable=True)
    data_pagamento = Column(DateTime, nullable=True)
    jatreino = Column(String(20), nullable=False)
    permissao = Column(String(30), nullable=False)
    observacao = Column(String(50), nullable=False)
    pagamento = Column(String(20), nullable=False)
    data_atualizacao = Column(DateTime, nullable=True)

    # Relacionamentos com cascade
    exercicios = relationship(
        "ExerciciosAluno", back_populates="aluno", cascade="all, delete-orphan"
    )
    medidas = relationship(
        "Medida", back_populates="aluno", cascade="all, delete-orphan"
    )
    progresso_semanal = relationship(
        "ProgressoSemanal", back_populates="aluno", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.senha = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    @property
    def inadimplente(self):
        if self.data_pagamento:
            prazo_pagamento = timedelta(days=32)
            data_limite = self.data_pagamento + prazo_pagamento
            if self.data_pagamento.month == datetime.now().month:
                data_limite += timedelta(days=1)
            tz_utc = timezone.utc
            data_atual_utc = datetime.now(tz=tz_utc)
            data_limite_utc = data_limite.replace(tzinfo=tz_utc)
            return data_atual_utc > data_limite_utc
        else:
            return True

    def __repr__(self):
        return (
            f"{self.id} {self.nome} {self.idade} {self.sexo} {self.telefone} "
            f"{self.login} {self.senha} {self.data_entrada} {self.data_pagamento} {self.jatreino} {self.permissao}"
        )


class ProgressoSemanal(Base):
    __tablename__ = "ProgressoSemanal"

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    dia = Column(String(50), nullable=False)
    tempo_treino = Column(Interval, nullable=False)
    pontos = Column(Integer, default=0)
    finalizado = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.now)

    aluno = relationship("Aluno", back_populates="progresso_semanal")


class Medida(Base):
    __tablename__ = "medidas"
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))
    peso = Column(String(30), nullable=False)
    ombro = Column(String(30), nullable=False)
    torax = Column(String(30), nullable=False)
    braco_d = Column(String(30), nullable=False)
    braco_e = Column(String(30), nullable=False)
    ant_d = Column(String(30), nullable=False)
    ant_e = Column(String(30), nullable=False)
    cintura = Column(String(30), nullable=False)
    abdome = Column(String(30), nullable=False)
    quadril = Column(String(30), nullable=False)
    coxa_d = Column(String(30), nullable=False)
    coxa_e = Column(String(30), nullable=False)
    pant_d = Column(String(30), nullable=False)
    pant_e = Column(String(30), nullable=False)
    data_atualizacao = Column(DateTime, nullable=True)

    aluno = relationship("Aluno", back_populates="medidas")

    def __repr__(self):
        return (
            f"{self.id} {self.aluno_id} {self.peso} {self.ombro} {self.torax} "
            f"{self.braco_d} {self.braco_e} {self.ant_d} {self.ant_e} {self.cintura} {self.abdome} "
            f"{self.quadril} {self.coxa_d} {self.coxa_e} {self.pant_d} {self.pant_e} {self.data_atualizacao}"
        )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    exercises = relationship(
        "Exercise", back_populates="category", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    tipoTreino = Column(String(80), nullable=False)
    exercicio = Column(String(80), nullable=False)
    serie = Column(String(80), nullable=False)
    repeticao = Column(String(80), nullable=False)
    descanso = Column(String(80), nullable=False)
    carga = Column(String(80), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="exercises")

    def to_dict(self):
        return {
            "id": self.id,
            "tipoTreino": self.tipoTreino,
            "exercicio": self.exercicio,
            "serie": self.serie,
            "repeticao": self.repeticao,
            "descanso": self.descanso,
            "carga": self.carga,
        }

    def __repr__(self):
        return (
            f"Exercise({self.tipoTreino}, {self.exercicio}, {self.serie}, "
            f"{self.repeticao}, {self.descanso}, {self.carga})"
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
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"))

    atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    aluno = relationship("Aluno", back_populates="exercicios")

    def __repr__(self):
        return f"{self.tipoTreino} {self.exercicio} {self.serie} {self.repeticao} {self.descanso} {self.carga} {self.atualizacao}"
