from typing import List
from src.database.models import Aluno, ExerciciosAluno
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.config import db_connector, DBConnectionHandler
from sqlalchemy.orm import joinedload, load_only


class Querys():
    # def __init__(self, connection):
    #     self.connection = connection
    def __init__(self, session):
        if session:
            self.session = session
        else:
            self.session = None

    def init_app(self, app):
        self.session = db.session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.session.remove()
    
    def mostrar_detalhes(self, aluno_id):
        return (
            self.session.query(Aluno)
            .options(joinedload(Aluno.exercicios))  # Carregamento da relação exercicios
            .filter_by(id=aluno_id)
            .first()
        )
    
    def mostrar(self, session):
        return session.query(Aluno).all()
        
   
    def deletar(self, aluno_id):
    
        # Restante do código...
        aluno = (
            self.session.query(Aluno)
            .options(joinedload(Aluno.exercicios))
            .filter_by(id=aluno_id)
            .first()
        )

        if aluno:
            self.session.query(ExerciciosAluno).filter_by(aluno_id=aluno.id).delete()
            self.session.delete(aluno)
            self.session.commit()

            return True
        else:
            return False

    def get_exercicios_by_aluno(self, aluno_id):
        exercicios = (
        self.session.query(ExerciciosAluno)
        .filter(ExerciciosAluno.aluno_id == aluno_id)
        .all()
        )
        return exercicios

    def verificar_credenciais(self, login, senha):
        # aluno = connection.query(Aluno).filter_by(login=login).first()
        aluno = (
            self.session.query(Aluno)
            .filter_by(login=login)
            .first()
        )
        if aluno and aluno.check_password(senha):
            return aluno, aluno.permissao  # Agora retorna o aluno e sua permissão

        return None, None 


    def cadastrar_aluno(self, nome, idade, sexo, altura, peso, email, telefone, login, senha, dia_semana, horario, inicio, obj, permissao, exercicios):
        aluno = Aluno(
            nome=nome, idade=idade, sexo=sexo, altura=altura, peso=peso, email=email, telefone=telefone,
            login=login, senha=generate_password_hash(senha), dia_semana=dia_semana, horario=horario,  inicio=inicio, obj=obj, permissao=permissao
        )

        self.session.add(aluno)

        for exercicio in exercicios:
            exercicio_aluno = ExerciciosAluno(
                tipoTreino=exercicio.get('tipoTreino', ''),
                exercicio=exercicio.get('exercicio', ''),
                serie=exercicio.get('serie', ''),
                repeticao=exercicio.get('repeticao', ''),
                descanso=exercicio.get('descanso', ''),
                carga=exercicio.get('carga', '')
            )
            aluno.exercicios.append(exercicio_aluno)

        self.session.commit()

        return aluno
   



