from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import  Querys
import json
from src.database.config import db_connector, DBConnectionHandler
from functools import wraps
from flask_login import current_user


cadastro_app = Blueprint("cadastro_app", __name__, url_prefix="/cadastro", template_folder='templates',static_folder='static')

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
@cadastro_app.route("/", methods=["GET", "POST"])
# @admin_required
def cadastrar():
  
    if request.method == 'POST':
        try:
            print(f'Recebendo dados: {request.form}')
            
            data = request.form.get('exercicios')
            exercicios = json.loads(data) if data else []
            
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            sexo = request.form.get('sexo')
            altura = request.form.get('altura')
            peso = request.form.get('peso')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            login = request.form.get('login')
            senha = request.form.get('senha')
            dia_semana = request.form.get('dia_semana')
            horario = request.form.get('horario')
            inicio = request.form.get('inicio')
            obj = request.form.get('obj')
            permissao = request.form.get('permissao')

            session = current_app.db.session
            # Crie uma instância da classe Querys
            querys_instance = Querys(session)

            # Chame o método cadastrar_aluno na instância
            querys_instance.cadastrar_aluno(
                nome, idade, sexo, altura, peso, email, telefone,
                login, senha, dia_semana, horario, inicio, obj, permissao,
                exercicios
            )

            return jsonify({'success': True}), 200

        except Exception as e:
            print(f'Erro no servidor: {str(e)}')
            return jsonify({'error': 'Erro no servidor'}), 500


    return render_template("cadastro.html")

  