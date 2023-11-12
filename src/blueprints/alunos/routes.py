from flask import Blueprint, request, render_template, url_for, redirect, current_app
from src.database.querys import Querys
# from flask_login import login_user, login_required, logout_user, current_user
from src.database.config import db, db_connector, DBConnectionHandler
from flask_login import current_user, login_required
from functools import wraps

clientes_app = Blueprint("clientes_app", __name__, url_prefix="/alunos", template_folder='templates',static_folder='static')

def admin_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'admin'."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.permissao == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_app.login'))
    return wrapper

# Tela Iniciarl do app
@clientes_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)  # Passe a sessão como argumento
        quantidade_alunos = len(alunos)
    return render_template("alunos.html", alunos=alunos, quantidade_alunos=quantidade_alunos)


@clientes_app.route("/detalhes/<int:aluno_id>", methods=["GET"])
@admin_required
def mostrar_detalhes(aluno_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        
        aluno = querys_instance.mostrar_detalhes(aluno_id) 
        
    return render_template('detalhes.html', aluno=[aluno])


@clientes_app.route("/deletar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def deletar(aluno_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar( aluno_id)
    return redirect(url_for("clientes_app.mostrar"))
   


# @clientes_app.route('/pesquisar_alunos', methods=['POST'])
# def pesquisar_alunos():
#     termo_pesquisa = request.form.get('termo_pesquisa', '').lower()
    
#     resultados = [aluno for aluno in alunos if termo_pesquisa in aluno['nome'].lower()]

#     return jsonify(resultados)