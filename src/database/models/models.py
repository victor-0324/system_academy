from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
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
    data_atualizacao = Column(DateTime, nullable=True)

    # Relacionamento com as tabelas ExerciciosAluno e Medidas
    exercicios = relationship('ExerciciosAluno', back_populates='aluno')
    medidas = relationship('Medida', back_populates='aluno')
    # Relacionamento com ProgressoCronometro
    progresso_cronometro = relationship('ProgressoCronometro', back_populates='aluno')

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

class Medida(Base):
    __tablename__ = "medidas"
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
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

    aluno = relationship('Aluno', back_populates='medidas')

    def __repr__(self):
        return (
            f"{self.id} {self.aluno_id} {self.peso} {self.ombro} {self.torax} "
            f"{self.braco_d} {self.braco_e} {self.ant_d} {self.ant_e} {self.cintura} {self.abdome} "
            f"{self.quadril} {self.coxa_d} {self.coxa_e} {self.pant_d} {self.pant_e} {self.data_atualizacao}"
        )

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    # Relacionamento com a tabela de exercícios
    exercises = relationship('Exercise', back_populates='category', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    tipoTreino = Column(String(80), nullable=False)
    exercicio = Column(String(80), nullable=False)
    serie = Column(String(80), nullable=False)
    repeticao = Column(String(80), nullable=False)
    descanso = Column(String(80), nullable=False)
    carga = Column(String(80), nullable=False)
    
    # Chave estrangeira para a tabela Category
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    # Relacionamento com a tabela de categorias
    category = relationship('Category', back_populates='exercises')

    def to_dict(self):
        return {
            'id': self.id,
            'tipoTreino': self.tipoTreino,
            'exercicio': self.exercicio,
            'serie': self.serie,
            'repeticao': self.repeticao,
            'descanso': self.descanso,
            'carga': self.carga,
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
    
    # Chave estrangeira referenciando a tabela Aluno
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    
    # Relacionamento com a tabela Aluno
    aluno = relationship('Aluno', back_populates='exercicios')

    def __repr__(self):
        return f"{self.tipoTreino} {self.exercicio} {self.serie} {self.repeticao} {self.descanso} {self.carga}"



class ProgressoCronometro(Base):
    __tablename__ = "progresso_cronometro"
    id = Column(Integer, primary_key=True)
    diaSemana = Column(String(10), nullable=False)  # Ex: 'Seg', 'Ter', etc.
    tempoTreino = Column(Float, nullable=False)  # Tempo em segundos
    estadoCronometro = Column(String(10), nullable=False)  # Ex: 'ativo', 'inativo'
    tempoTotalSemana = Column(Float, nullable=False)  # Tempo acumulado na semana
    dataInicio = Column(DateTime)  # Data e hora de início do cronômetro
    dataAtualizacao = Column(DateTime, default=datetime.utcnow)
    
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    aluno = relationship('Aluno', back_populates='progresso_cronometro')

    def __repr__(self):
        return f"{self.diaSemana} {self.tempoTreino} {self.estadoCronometro} {self.tempoTotalSemana} {self.dataInicio}"




# ALTER TABLE alunos DROP COLUMN peso;
# ALTER TABLE alunos DROP COLUMN ombro;
# ALTER TABLE alunos DROP COLUMN torax;
# ALTER TABLE alunos DROP COLUMN braco_d;
# ALTER TABLE alunos DROP COLUMN braco_e;
# ALTER TABLE alunos DROP COLUMN ant_d;
# ALTER TABLE alunos DROP COLUMN ant_e;
# ALTER TABLE alunos DROP COLUMN cintura;
# ALTER TABLE alunos DROP COLUMN abdome;
# ALTER TABLE alunos DROP COLUMN quadril;
# ALTER TABLE alunos DROP COLUMN coxa_d;
# ALTER TABLE alunos DROP COLUMN coxa_e;
# ALTER TABLE alunos DROP COLUMN pant_d;
# ALTER TABLE alunos DROP COLUMN pant_e;
# ALTER TABLE alunos DROP COLUMN historico_medidas_peso;

# INSERT INTO medidas (
#     aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, data_atualizacao
# )
# SELECT
#     id, 
#     peso,
#     ombro,
#     torax,
#     braco_d,
#     braco_e,
#     ant_d,
#     ant_e,
#     cintura,
#     abdome,
#     quadril,
#     coxa_d,
#     coxa_e,
#     pant_d,
#     pant_e,
#     data_atualizacao
# FROM alunos;


# from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime, JSON
# from sqlalchemy.orm import relationship, sessionmaker
# from flask_login import UserMixin, login_manager
# from werkzeug.security import check_password_hash, generate_password_hash
# from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
# from src.database import Base
# from datetime import datetime, timedelta, timezone

# class Aluno(Base):
#     __tablename__ = "alunos"
#     id = Column(Integer, primary_key=True)
#     nome = Column(String(80), nullable=False)
#     idade = Column(DateTime, nullable=True)
#     sexo = Column(String(30), nullable=False)
#     peso = Column(String(30), nullable=False)
#     ombro = Column(String(30), nullable=False)
#     torax = Column(String(30), nullable=False)
#     braco_d = Column(String(30), nullable=False)
#     braco_e = Column(String(30), nullable=False)
#     ant_d = Column(String(30), nullable=False)
#     ant_e = Column(String(30), nullable=False)
#     cintura = Column(String(30), nullable=False)
#     abdome = Column(String(30), nullable=False)
#     quadril = Column(String(30), nullable=False)
#     coxa_d = Column(String(30), nullable=False)
#     coxa_e = Column(String(30), nullable=False)
#     pant_d = Column(String(30), nullable=False)
#     pant_e = Column(String(30), nullable=False)
#     observacao = Column(String(50), nullable=False)
#     telefone = Column(String(30), nullable=False)
#     login = Column(String(30), nullable=False)
#     senha = Column(String(50), nullable=False)
#     data_entrada = Column(DateTime, nullable=True)
#     data_pagamento = Column(DateTime, nullable=True)
#     jatreino = Column(String(20), nullable=False)
#     permissao = Column(String(30), nullable=False)
#     historico_medidas_peso = Column(JSON, nullable=True) 
#     data_atualizacao = Column(DateTime) 

#     def set_password(self, password):
#         self.senha = generate_password_hash(password, method="sha256")

#     def check_password(self, password):
#         return check_password_hash(self.senha, password)

#     def is_active(self):
#         # Aqui você pode implementar a lógica para verificar se o aluno está ativo
#         return True 
#     # Adicionando métodos necessários para Flask-Login
#     def get_id(self):
#         return str(self.id)

#     def is_authenticated(self):
#         return True  # ou implemente a lógica desejada

#     def is_anonymous(self):
#         return False

#     # Relacionamento com a tabela ExerciciosAluno
#     exercicios = relationship('ExerciciosAluno', back_populates='aluno')
    
#     def medidas_historico(self):
#         historico_antes = []
#         historico_depois = []

#         if self.data_entrada:
#             historico_antes.append(self._medidas_dict(descricao='Entrada', data=self.data_entrada))

#         if self.data_atualizacao:
#             historico_depois.append(self._medidas_dict(descricao='Atualização', data=self.data_atualizacao))

#         return historico_antes + historico_depois

#     def _medidas_dict(self, **kwargs):
#         medidas_dict = {
#             'peso': (self.peso),
#             'ombro': (self.ombro),
#             'torax': (self.torax),
#             'braco_d': (self.braco_d),
#             'braco_e': (self.braco_e),
#             'ant_d': (self.ant_d),
#             'ant_e': (self.ant_e),
#             'cintura': (self.cintura),
#             'abdome': (self.abdome),
#             'quadril': (self.quadril),
#             'coxa_d': (self.coxa_d),
#             'coxa_e': (self.coxa_e),
#             'pant_d': (self.pant_d),
#             'pant_e': (self.pant_e),
#             'data_entrada': self.data_entrada.strftime('%Y-%m-%d') if self.data_entrada else None,
#             'data_atualizacao': self.data_atualizacao.strftime('%Y-%m-%d') if self.data_atualizacao else None,
#         }
        
#         # medidas_dict.update(kwargs)  # Atualiza o dicionário com argumentos adicionais
#         return medidas_dict

#     @property
#     def inadimplente(self):
#         if self.data_pagamento:
#             prazo_pagamento = timedelta(days=31)

#             # Calcular a data limite com base na última data de pagamento
#             data_limite = self.data_pagamento + prazo_pagamento

#             # Verificar se o mês atual tem mais de 30 dias e adicionar um dia extra se necessário
#             if self.data_pagamento.month == datetime.now().month:
#                 data_limite += timedelta(days=1)

#             # Obtém o fuso horário UTC
#             tz_utc = timezone.utc

#             # Obtém a data e hora atual com o fuso horário UTC
#             data_atual_utc = datetime.now(tz=tz_utc)

#             # Converte a data de limite para o fuso horário UTC
#             data_limite_utc = data_limite.replace(tzinfo=tz_utc)

#             # Verifica se a data atual é maior que a data limite
#             return data_atual_utc > data_limite_utc
#         else:
#             return True


#     def __repr__(self):
#         return (
#         f"{self.id} {self.nome} {self.idade} {self.sexo} {self.peso} "
#         f"{self.ombro} {self.torax} {self.braco_d} {self.braco_e} {self.ant_d} {self.ant_e} {self.cintura} {self.abdome} "
#         f"{self.quadril} {self.coxa_d} {self.coxa_e} {self.pant_d} {self.pant_e} {self.observacao} {self.telefone} "
#         f"{self.login} {self.senha} {self.data_entrada} {self.data_pagamento} {self.jatreino} {self.permissao}"
#          )

# class ExerciciosAluno(Base):
#     __tablename__ = "exercicios_aluno"
#     id = Column(Integer, primary_key=True)
#     tipoTreino = Column(String(80), nullable=False)
#     exercicio = Column(String(80), nullable=False)
#     serie = Column(String(80), nullable=False)
#     repeticao = Column(String(80), nullable=False)
#     descanso = Column(String(80), nullable=False)
#     carga = Column(String(80), nullable=False)
    
#     # Chave estrangeira referenciando a tabela Aluno
#     aluno_id = Column(Integer, ForeignKey('alunos.id'))
    
#     # Relacionamento com a tabela Aluno
#     aluno = relationship('Aluno', back_populates='exercicios')

#     def __repr__(self):
#         return f"{self.tipoTreino} {self.exercicio} {self.serie} {self.repeticao} {self.descanso} {self.carga}"