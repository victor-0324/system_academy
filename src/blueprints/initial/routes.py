from flask import Blueprint, request, render_template, url_for, redirect, current_app
from src.database.querys import Querys
from functools import wraps
from flask_login import current_user
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
from src.database.sheets.sheets import SheetsConnector
from uuid import UUID

initial_app = Blueprint("initial_app", __name__, url_prefix="/", template_folder='templates',static_folder='static')

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

# def calcular_proxima_data_pagamento(data_pagamento_atual):
#     if data_pagamento_atual:
#         # Converter a string da data atual para um objeto datetime
#         data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')

#         # Calcular a próxima data de pagamento (por exemplo, mensalmente)
#         proxima_data_pagamento = data_pagamento_atual + relativedelta(months=1)

#         # Formatando a próxima data de pagamento como string
       
#         proxima_data_pagamento_str = proxima_data_pagamento.strftime('%d/%m/%Y')
#         return proxima_data_pagamento_str

#     return None
    
# Tela Iniciarl do app
@initial_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    with current_app.app_context():
        # session = current_app.db.session
        # querys_instance = Querys(session)
        # alunos = querys_instance.mostrar(session)
        admin = current_user.id
        sheets_connector = SheetsConnector() 

        alunos = sheets_connector.obter_todos_alunos()

        alunos_pagam_semana = []
        inadimplentes = []

        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno["Data_pagamento"]
            
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = sheets_connector.calcular_inadimplencia(aluno)
           
            if proxima_data_pagamento:
                # Converta proxima_data_pagamento para datetime para comparação
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                
                # Comparar se a próxima data de pagamento está nos próximos 7 dias
                data_limite = datetime.now() + timedelta(days=7)
                
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'nome': aluno["Nome"],
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            if inadimplente is True:
                data_pagamento_atual_str = aluno["Data_pagamento"]
                inadimplentes.append({
                    'nome': aluno["Nome"],
                    'dataPagamento': data_pagamento_atual_str
                })
            

        quantidade_alunos = len(alunos)
    return render_template("index.html", alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, quantidade_alunos=quantidade_alunos)