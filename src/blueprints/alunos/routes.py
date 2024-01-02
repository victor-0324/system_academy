from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import Querys
from datetime import datetime, timedelta
from src.database.config import db, db_connector, DBConnectionHandler
from flask_login import current_user, login_required
from functools import wraps
from dateutil.relativedelta import relativedelta 
import json
from copy import deepcopy 
from src.database.sheets.sheets import SheetsConnector


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
        # Verificar se data_pagamento_atual já é uma string
        if isinstance(data_pagamento_atual, str):
            # Converter a string da data atual para um objeto datetime
            data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')

        # Calcular a próxima data de pagamento (por exemplo, mensalmente)
        proxima_data_pagamento = data_pagamento_atual + timedelta(days=30)

        # Formatando a próxima data de pagamento como string
        proxima_data_pagamento_str = proxima_data_pagamento.strftime('%d/%m/%Y')
        return proxima_data_pagamento_str

    return None

# Tela Iniciarl do app
@clientes_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    with current_app.app_context():
        sheets_connector = SheetsConnector()
        alunos_sheets = sheets_connector.obter_todos_alunos()

        # Inicializar listas para armazenar informações sobre cada aluno
        data_pagamento_atual_list = []
        proxima_data_pagamento_list = []
        inadimplente_list = []
        
        # Iterar sobre cada aluno na lista
        for aluno in alunos_sheets:
            # Obter apenas a data de pagamento do aluno
            data_pagamento = aluno.get('Data_pagamento')

            if data_pagamento:
                if isinstance(data_pagamento, str):
                    # Se for uma string, converte para datetime
                    aluno['Data_pagamento'] = datetime.strptime(data_pagamento, '%Y-%m-%dT%H:%M:%S.%fZ')
                elif isinstance(data_pagamento, datetime):
                    # Se já for um datetime, mantém como está
                    aluno['Data_pagamento'] = data_pagamento
            else:
                aluno['Data_pagamento'] = None
            
            # Adicionar a data de pagamento atual à lista
            data_pagamento_atual_list.append(aluno['Data_pagamento'])

            # Calcular a próxima data de pagamento (certifique-se de implementar essa função)
            proxima_data_pagamento = calcular_proxima_data_pagamento(aluno['Data_pagamento'])
            proxima_data_pagamento_list.append(proxima_data_pagamento)

            # Verificar se o aluno é inadimplente
            inadimplente = sheets_connector.calcular_inadimplencia(aluno)
            inadimplente_list.append(inadimplente)

        # Passar as listas para o template
        return render_template("alunos.html", alunos=alunos_sheets, quantidade_alunos=len(alunos_sheets),
                               data_pagamento_atual_list=data_pagamento_atual_list,
                               proxima_data_pagamento_list=proxima_data_pagamento_list,
                               inadimplente_list=inadimplente_list) 

@clientes_app.route("/detalhes/<string:aluno_id>", methods=["GET"])
@admin_required
def mostrar_detalhes(aluno_id):
    with current_app.app_context():
        sheets_connector = SheetsConnector()

        # Obter detalhes do aluno da planilha
        aluno = sheets_connector.obter_aluno_por_id(str(aluno_id))
        # aluno = sheets_connector.obter_aluno_por_id(aluno_id)
        
        if not aluno:
            # Tratar caso o aluno não seja encontrado
            return render_template('404.html'), 404

        # Obter apenas a data de pagamento do aluno
        data_pagamento_atual = aluno.get('Data_pagamento')
        
        # Calcular a próxima data de pagamento
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
        
        # Verificar se o aluno é inadimplente
        inadimplente = sheets_connector.calcular_inadimplencia(aluno)

    return render_template('detalhes.html', aluno=aluno, inadimplente=inadimplente, proxima_data_pagamento=proxima_data_pagamento, data_pagamento_atual=data_pagamento_atual)
# @admin_required
# def mostrar_detalhes(aluno_id):
#     with current_app.app_context():
#         session = current_app.db.session
#         querys_instance = Querys(session)
#         aluno = querys_instance.mostrar_detalhes(aluno_id) 
#         # Obter apenas a data de pagamento do aluno
#         data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
#         # Calcular a próxima data de pagamento
#         proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
        
#         # Verificar se o aluno é inadimplente
#         inadimplente = aluno.inadimplente
#     return render_template('detalhes.html', aluno=[aluno], inadimplente=inadimplente, proxima_data_pagamento=proxima_data_pagamento, data_pagamento_atual=data_pagamento_atual)


@clientes_app.route("/atualizar/<string:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar(aluno_id):
    sheets_connector = SheetsConnector()
    # session = current_app.db.session
    # querys_instance = Querys(session)

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

            # Atualize o aluno e adicione as novas medidas à coluna "Medidas"
            sheets_connector.atualizar_aluno(aluno_id, peso, ombro, torax, braco_d, braco_e, 
                                    ant_d, ant_e,
                                    cintura, abdome, quadril, coxa_d, coxa_e, pant_d, pant_e,
                                    observacao, telefone, login, data_pagamento, senha, exercicios
                                    )
           
            return jsonify({'success': True}), 200

        else:
            aluno = sheets_connector.obter_aluno_por_id(aluno_id)
            return render_template("modificar.html", aluno=[aluno])

    except Exception as e:
        print(f'Erro no servidor: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500


        
# @clientes_app.route("/atualizar/<string:aluno_id>", methods=["GET", "POST"])
# @admin_required
# def atualizar(aluno_id):
#     sheets_connector = SheetsConnector()
#     session = current_app.db.session
#     querys_instance = Querys(session)
#     try:
#         if request.method == "POST":
#             data = request.form.get('exercicios')
#             exercicios = json.loads(data) if data else []
#             peso = request.form.get("peso")
#             ombro = request.form.get("ombro")
#             torax = request.form.get("torax")
#             braco_d = request.form.get("braco_d")
#             braco_e = request.form.get("braco_e")
#             ant_d = request.form.get("ant_d")
#             ant_e = request.form.get("ant_e")
#             cintura = request.form.get("cintura")
#             abdome = request.form.get("abdome")
#             quadril = request.form.get("quadril")
#             coxa_d = request.form.get("coxa_d")
#             coxa_e = request.form.get("coxa_e")
#             pant_d = request.form.get("pant_d")
#             pant_e = request.form.get("pant_e")
#             observacao = request.form.get("observacao")
#             telefone = request.form.get("telefone")
#             login = request.form.get("login")
#             senha = request.form.get("senha")
#             data_pagamento = request.form.get("data_pagamento")
           
            
#             medidas = sheets_connector.atualizar_medidas(
#                 aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
#                 abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, data_pagamento, senha, exercicios
#             )

#             aluno = sheets_connector.obter_aluno_por_id(str(aluno_id))
#             # dados_aluno["Aluno_id"] = aluno
#             print(aluno)
#             # Adicione as medidas como um JSON
#             # medidas_json = json.dumps(dados_aluno.get("Medidas", {}))
#             # Use a função atualizar_dados para atualizar as informações do aluno
#             # aluno_antes = deepcopy(aluno)  # Crie uma cópia profunda do aluno antes da atualização
#             # historico_antes, historico_depois = sheets_connector.atualizar_dados(
#             #     aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
#             #     abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, data_pagamento, senha, exercicios
#             # )
            
#             return jsonify({'success': True, 'historico_antes': historico_antes, 'historico_depois': historico_depois}), 200

#         else:
#             aluno = sheets_connector.obter_aluno_por_id(aluno_id)
#             return render_template("modificar.html", aluno=[aluno])

#     except Exception as e:
#         print(f'Erro no servidor: {str(e)}')
#         return jsonify({'error': 'Erro no servidor'}), 500



@clientes_app.route("/deletar/<string:aluno_id>", methods=["GET", "POST"])
@admin_required
def deletar(aluno_id):
    with current_app.app_context():
        sheets_connector = SheetsConnector() 

        # Deletar o aluno
        sheets_connector.deletar_aluno(aluno_id)

        # session = current_app.db.session
        # querys_instance = Querys(session)
        # querys_instance.deletar( aluno_id)
    return redirect(url_for("clientes_app.mostrar"))
   

