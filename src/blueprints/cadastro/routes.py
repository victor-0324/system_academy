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
            data = request.form.get('exercicios')
            exercicios = json.loads(data) if data else []
            
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            sexo = request.form.get('sexo')
           
            peso = request.form.get('peso')
            ombro_d = request.form.get('ombro_d')
            ombro_e = request.form.get('ombro_e')
            torax = request.form.get('torax')
            braco_d = request.form.get('braco_d')
            braco_e = request.form.get('braco_e')
            ant_d = request.form.get('ant_d')
            ant_e = request.form.get('ant_e')
            cintura = request.form.get('cintura')
            abdome = request.form.get('abdome')
            quadril = request.form.get('quadril')
            coxa_d = request.form.get('coxa_d')
            coxa_e = request.form.get('coxa_e')
            pant_d = request.form.get('pant_d')
            pant_e = request.form.get('pant_e')
            observacao = request.form.get('observacao')
            telefone = request.form.get('telefone')
            login = request.form.get('login')
            senha = request.form.get('senha')
            data_entrada = request.form.get('data_entrada')
            data_pagamento = request.form.get('data_pagamento')
            jatreino = request.form.get('jatreino')
            permissao = request.form.get('permissao')

            session = current_app.db.session
            # Crie uma instância da classe Querys
            querys_instance = Querys(session)

            # Chame o método cadastrar_aluno na instância
            querys_instance.cadastrar_aluno(
                nome, idade, sexo, peso, ombro_d, ombro_e, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, senha,
                data_entrada, data_pagamento, jatreino, permissao,
                exercicios
            )

            return jsonify({'success': True}), 200

        except Exception as e:
            print(f'Erro no servidor: {str(e)}')
            return jsonify({'error': 'Erro no servidor'}), 500

    return render_template("cadastro.html")

  