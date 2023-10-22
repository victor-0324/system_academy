from typing import List
from src.database.config import DBConnectionHendler, db_connector
from src.database.models import Treino, Aluno

class Querys():
    @classmethod
    @db_connector
    def get_alunos(cls, connection, treino, nome):
        aluno = Aluno(
            nome = nome.upper(), treino=treino
        )
        connection.session.add(aluno)
        connection.session.commit()

        return Aluno.query.all()

    @classmethod
    @db_connector
    def get_treinos_aluno(aluno_id):
        return Treino.query.filter_by(aluno_id=aluno_id).all()

    @classmethod
    @db_connector
    def cadastrar_aluno(nome):
        aluno = Aluno(nome=nome)
        db.session.add(aluno)
        db.session.commit()
        return aluno

    @classmethod
    @db_connector
    def cadastrar_treino(descricao, aluno_id):
        treino = Treino(descricao=descricao, aluno_id=aluno_id)
        db.session.add(treino)
        db.session.commit()
        return treino