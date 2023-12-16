from flask import Blueprint, render_template, flash, redirect, url_for,current_app, request, abort
from flask_login import current_user, login_required
from src.database.querys import Querys
from functools import wraps
from src.database.config import DBConnectionHandler, db
from src.database.models import Aluno
from datetime import datetime

treino_app = Blueprint("treino_app", __name__, url_prefix="/treino", template_folder='templates', static_folder='static')


def formatar_data(data):
    if data is None:
        return "Inicio Da Evolução"
    return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")



def treino_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'treino' e que não estão inadimplentes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.permissao == 'treino' and not current_user.inadimplente:
            return func(*args, **kwargs)
        else:
            flash("Você não tem permissão para acessar esta página. Verifique seu status de pagamento.")
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

@treino_app.route("/evolucao/<int:aluno_id>", methods=["GET"])
@treino_required
def evolucao(aluno_id):
    session = current_app.db.session
    querys_instance = Querys(session)

    aluno = querys_instance.session.query(Aluno).filter_by(id=aluno_id).first()

    if aluno:
        historico = aluno.medidas_historico()
        historico_medidas_peso = aluno.historico_medidas_peso
        historico_depois = [historico[-1]]  
       
        return render_template('evolucao.html', historico_medidas_peso=historico_medidas_peso, historico_depois=historico_depois,formatar_data=formatar_data)
    else:
        # Retorna uma página de erro 404
        abort(404) 