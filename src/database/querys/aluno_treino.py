from typing import List
from src.database.config import DBConnectionHendler, db_connector
from src.database.models import Aluno

class Querys():

    @classmethod
    @db_connector
    def mostrar(cls, connection):
        """Retorna uma lista de todos os clientes"""
        mostrar = connection.session.query(Aluno) 
        mostrar = mostrar.all()
        return mostrar

    @classmethod
    @db_connector
    def mostrar_detalhes(cls, connection, aluno_id):
        # Recuperar detalhes do aluno com base no ID        
        return connection.session.query(Aluno).filter_by(id=aluno_id)
        
    @classmethod
    @db_connector
    def deletar(cls, connection, aluno_id):
        """someting"""
        cliente = connection.session.query(Aluno).filter_by(id=aluno_id).first()
        connection.session.delete(cliente)
        connection.session.commit()


    @classmethod
    @db_connector
    def cadastrar_aluno(cls, connection, nome, idade, sexo, altura, peso, email, telefone, login, senha, dia_semana, tipo_treino, horario, inicio, obj):
        aluno = Aluno(
            nome=nome, idade=idade, sexo=sexo, altura=altura, peso=peso, email=email, telefone=telefone, login=login, senha=senha, dia_semana=dia_semana,
            tipo_treino=tipo_treino, horario=horario, inicio=inicio, obj=obj
        )
        connection.session.add(aluno)
        connection.session.commit()
        return aluno

