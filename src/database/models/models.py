from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime, JSON
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

    def medidas_historico(self):
        historico_antes = []
        historico_depois = []

        if self.data_entrada:
            historico_antes.append(self._medidas_dict(descricao='Entrada', data=self.data_entrada))

        if self.data_atualizacao:
            historico_depois.append(self._medidas_dict(descricao='Atualização', data=self.data_atualizacao))

        return historico_antes + historico_depois

    def _medidas_dict(self, **kwargs):
        medidas_dict = {
            
            'peso': (self.peso),
            'ombro_d': (self.ombro_d),
            'ombro_e': (self.ombro_e),
            'torax': (self.torax),
            'braco_d': (self.braco_d),
            'braco_e': (self.braco_e),
            'ant_d': (self.ant_d),
            'ant_e': (self.ant_e),
            'cintura': (self.cintura),
            'abdome': (self.abdome),
            'quadril': (self.quadril),
            'coxa_d': (self.coxa_d),
            'coxa_e': (self.coxa_e),
            'pant_d': (self.pant_d),
            'pant_e': (self.pant_e),
            'data_entrada': self.data_entrada.strftime('%Y-%m-%d') if self.data_entrada else None,
            'data_atualizacao': self.data_atualizacao.strftime('%Y-%m-%d') if self.data_atualizacao else None,
        }
        
        # medidas_dict.update(kwargs)  # Atualiza o dicionário com argumentos adicionais
        return medidas_dict
        
    def __repr__(self):
        return (
        f"{self.id} {self.nome} {self.idade} {self.sexo} {self.peso} "
        f"{self.ombro_d} {self.ombro_e} {self.torax} {self.braco_d} {self.braco_e} {self.ant_d} {self.ant_e} {self.cintura} {self.abdome} "
        f"{self.quadril} {self.coxa_d} {self.coxa_e} {self.pant_d} {self.pant_e} {self.observacao} {self.telefone} "
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
 