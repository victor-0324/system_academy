
from .models import db, Aluno, Treino

class Querys():
    def get_alunos():
        return Aluno.query.all()

    def get_treinos_aluno(aluno_id):
        return Treino.query.filter_by(aluno_id=aluno_id).all()

    def cadastrar_aluno(nome):
        aluno = Aluno(nome=nome)
        db.session.add(aluno)
        db.session.commit()
        return aluno

    def cadastrar_treino(descricao, aluno_id):
        treino = Treino(descricao=descricao, aluno_id=aluno_id)
        db.session.add(treino)
        db.session.commit()
        return treino