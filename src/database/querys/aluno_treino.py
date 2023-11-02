from typing import List
from src.database.config import DBConnectionHendler, db_connector
from src.database.models import Aluno, ExerciciosAluno

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
        aluno = connection.session.query(Aluno).filter_by(id=aluno_id).first()

        if aluno:
            # Deletar os exercícios associados ao aluno
            connection.session.query(ExerciciosAluno).filter_by(aluno_id=aluno.id).delete()
            # Deletar o aluno
            connection.session.delete(aluno)
            # Commit das alterações
            connection.session.commit()
            return True  # Indica que a deleção foi bem-sucedida
        return False


    @classmethod
    @db_connector
    def cadastrar_aluno(cls, connection, nome, idade, sexo, altura, peso, email, telefone, login, senha, dia_semana, horario, inicio, obj, exercicios):
        aluno = Aluno(
            nome=nome, idade=idade, sexo=sexo, altura=altura, peso=peso, email=email, telefone=telefone,
            login=login, senha=senha, dia_semana=dia_semana, horario=horario,  inicio=inicio, obj=obj
        )

        connection.session.add(aluno)
        connection.session.commit()

        for exercicio in exercicios:
            exercicio_aluno = ExerciciosAluno(
                aluno_id=aluno.id,
                tipoTreino=exercicio.get('tipoTreino', ''),
                exercicio=exercicio.get('exercicio', ''),
                serie=exercicio.get('serie', ''),
                repeticao=exercicio.get('repeticao', ''),
                descanso=exercicio.get('descanso', ''),
                carga=exercicio.get('carga', '')
            )
            connection.session.add(exercicio_aluno)

        connection.session.commit()

        return aluno

