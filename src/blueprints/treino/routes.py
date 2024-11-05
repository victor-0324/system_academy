from flask import Blueprint, render_template, flash, redirect, url_for,current_app, request, abort, json, jsonify
from flask_login import current_user, login_required
from src.database.querys import Querys
from functools import wraps
from src.database.config import DBConnectionHandler, db
from src.database.models import Aluno
import locale
from datetime import datetime, timedelta

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
            
            return redirect(url_for('login_app.login'))
    return wrapper

def calcular_proxima_data_pagamento(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data de pagamento atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')

        # Calcular a próxima data de pagamento com base em 30 dias de inadimplência
        proxima_data_pagamento = data_pagamento_atual + timedelta(days=30)

        # Verificar se o mês atual tem mais de 30 dias e adicionar um dia extra se necessário
        if data_pagamento_atual.month == proxima_data_pagamento.month:
            proxima_data_pagamento += timedelta(days=1)

        # Formatando a próxima data de pagamento como string
        proxima_data_pagamento_str = proxima_data_pagamento.strftime('%d/%m/%Y')
        return proxima_data_pagamento_str

    return None

@treino_app.route("/", methods=["GET", "POST"])
@treino_required
def mostrar():
    # Recupere o ID do aluno da URL
    aluno_id = current_user.id
    
    # Agora, use o aluno_id para recuperar os treinos específicos do aluno
    session = current_app.db.session
    querys_instance = Querys(session)
    aluno = querys_instance.mostrar_detalhes(aluno_id)
    exercicios = querys_instance.get_exercicios_by_aluno(aluno_id)
    aluno = querys_instance.session.query(Aluno).filter_by(id=aluno_id).first()
    data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
    proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
    with open('src/static/manifest.json', 'r') as file:
        manifest = json.load(file)
        
    # Verificação de pagamento
    faltam_tres_dias = querys_instance.verificar_falta_tres_dias(aluno_id)
    return render_template('aluno_treino.html',proxima_data_pagamento=proxima_data_pagamento,
                            exercicios=exercicios,
                            faltam_tres_dias=faltam_tres_dias,
                            aluno=aluno, manifest=manifest)

@treino_app.route("/evolucao/<int:aluno_id>", methods=["GET"])
@treino_required
def evolucao(aluno_id):
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

    session = current_app.db.session
    querys_instance = Querys(session)
    aluno = querys_instance.session.query(Aluno).filter_by(id=aluno_id).first()
    
    if aluno:
        medidas = querys_instance.get_medidas_por_aluno(aluno_id)
        
        # Verificar se as medidas foram carregadas
        if not medidas:
            return render_template('evolucao.html', aluno=aluno, manifest=manifest, medidas=[])

        # Garantir que todos os valores de data_atualizacao são do tipo datetime
        for medida in medidas:
            if medida['data_atualizacao'] is not None:
                if isinstance(medida['data_atualizacao'], str):
                    medida['data_atualizacao'] = datetime.strptime(medida['data_atualizacao'], "%Y-%m-%d %H:%M:%S")
                elif not isinstance(medida['data_atualizacao'], datetime):
                    medida['data_atualizacao'] = datetime.fromtimestamp(medida['data_atualizacao'])

        # Filtrar medidas onde data_atualizacao não é None
        medidas = [m for m in medidas if m['data_atualizacao'] is not None]
       
        # Ordenar por data
        medidas.sort(key=lambda x: x['data_atualizacao'], reverse=True)  # Ordenar do mais recente para o mais antigo

        return render_template(
            'evolucao.html',
            aluno=aluno,
            medidas=medidas,
            manifest=manifest
        )
    else:
        abort(404)

        # asdfas
