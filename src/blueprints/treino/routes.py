from flask import Blueprint, render_template, flash, redirect, url_for,current_app, request
from flask_login import current_user, login_required
from src.database.querys import Querys
from functools import wraps
from src.database.config import DBConnectionHandler, db

treino_app = Blueprint("treino_app", __name__, url_prefix="/treino", template_folder='templates', static_folder='static')


def treino_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'treino'."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.permissao == 'treino':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_app.login'))
    return wrapper


@treino_app.route("/", methods=["GET", "POST"])
@treino_required
def mostrar():
    # Recupere o ID do aluno da URL
    aluno_id = current_user.id

    # Agora, use o aluno_id para recuperar os treinos específicos do aluno
    session = current_app.db.session
    querys_instance = Querys(session)

    exercicios = querys_instance.get_exercicios_by_aluno(aluno_id)

    return render_template('treinos_alunos.html', exercicios=exercicios)
  
