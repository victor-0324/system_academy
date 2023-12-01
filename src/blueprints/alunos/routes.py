from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import Querys
from datetime import datetime
from src.database.config import db, db_connector, DBConnectionHandler
from flask_login import current_user, login_required
from functools import wraps
from dateutil.relativedelta import relativedelta 
import json
from copy import deepcopy 


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

def calcular_proxima_data_pagamento(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')

        # Calcular a próxima data de pagamento (por exemplo, mensalmente)
        proxima_data_pagamento = data_pagamento_atual + relativedelta(months=1)

        # Formatando a próxima data de pagamento como string
       
        proxima_data_pagamento_str = proxima_data_pagamento.strftime('%d/%m/%Y')
        return proxima_data_pagamento_str

    return None

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

        # Obter apenas a data de pagamento do aluno
        data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None

        # Calcular a próxima data de pagamento
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)

    return render_template('detalhes.html', aluno=[aluno],  proxima_data_pagamento=proxima_data_pagamento)

@clientes_app.route("/atualizar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar(aluno_id):
    session = current_app.db.session
    querys_instance = Querys(session)
    try:
        if request.method == "POST":
            data = request.form.get('exercicios')
            exercicios = json.loads(data) if data else []
            peso = request.form.get("peso")
            ombro = request.form.get("ombro")
            torax = request.form.get("torax")
            braco_d = request.form.get("braco_d")
            braco_e = request.form.get("braco_e")
            ant_d = request.form.get("ant_d")
            ant_e = request.form.get("ant_e")
            cintura = request.form.get("cintura")
            abdome = request.form.get("abdome")
            quadril = request.form.get("quadril")
            coxa_d = request.form.get("coxa_d")
            coxa_e = request.form.get("coxa_e")
            pant_d = request.form.get("pant_d")
            pant_e = request.form.get("pant_e")
            observacao = request.form.get("observacao")
            telefone = request.form.get("telefone")
            login = request.form.get("login")
            senha = request.form.get("senha")
            data_pagamento = request.form.get("data_pagamento")
            opcaoExercicio = request.form.get("opcaoExercicio")
            
            if not all([ peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                        abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, telefone, login]):
                raise ValueError("Preencha todos os campos obrigatórios.")

            aluno = querys_instance.mostrar_detalhes(aluno_id)

            # Use a função atualizar_dados para atualizar as informações do aluno
            aluno_antes = deepcopy(aluno)  # Crie uma cópia profunda do aluno antes da atualização
            historico_antes, historico_depois = querys_instance.atualizar_dados(
                aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, data_pagamento, senha, exercicios
            )
            
            return jsonify({'success': True, 'historico_antes': historico_antes, 'historico_depois': historico_depois}), 200

        else:
            aluno = querys_instance.mostrar_detalhes(aluno_id)
            return render_template("modificar.html", aluno=[aluno])

    except Exception as e:
        print(f'Erro no servidor: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500

@clientes_app.route("/deletar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def deletar(aluno_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar( aluno_id)
    return redirect(url_for("clientes_app.mostrar"))
   

