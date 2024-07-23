from flask import Blueprint, request, render_template, url_for, redirect, current_app, send_file, jsonify, json
from src.database.querys import Querys
from functools import wraps
from flask_login import current_user
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 

initial_app = Blueprint("initial_app", __name__, url_prefix="/", template_folder='templates',static_folder='static')

@initial_app.route('/sw.js')
def serve_sw():
    return send_file('static/sw.js', mimetype='application/javascript')


@initial_app.route('/manifest.json')
def serve_manifest():
    return send_file('static/manifest.json', mimetype='application/manifest+json')


# @initial_app.route('/offline')
# def offline():
#     return jsonify({"response": 0})

@initial_app.route('/app')
def index1():
    with open('src/static/manifest.json', 'r') as file:
        manifest = json.load(file)
    return render_template("index1.html", manifest=manifest)

@initial_app.route('/manifest.json')
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


def calcular_proxima_atualizacao(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data de pagamento atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, '%Y-%m-%d')

        # Calcular a próxima data de pagamento com base em 30 dias de inadimplência
        proxima_atualizacao = data_pagamento_atual + timedelta(days=60)

        # Verificar se o mês atual tem mais de 30 dias e adicionar um dia extra se necessário
        if data_pagamento_atual.month == proxima_atualizacao.month:
            proxima_atualizacao += timedelta(days=1)

        # Formatando a próxima data de pagamento como string
        proxima_atualizacao_str = proxima_atualizacao.strftime('%d/%m/%Y')
        return proxima_atualizacao_str

    return None
# Tela Iniciarl do app
@initial_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)

        alunos_pagam_semana = []
        inadimplentes = []
        proxima_data_pagamento_list = []
        alunos_atualizar_medidas = []
        total_alunos_ativos = 0
        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente
            
            if inadimplente:
                proxima_data_pagamento_list.append(proxima_data_pagamento)

            if not inadimplente:
                total_alunos_ativos += 1

            if proxima_data_pagamento:
                # Converta proxima_data_pagamento para datetime para comparação
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                data_limite = datetime.now() + timedelta(days=6)
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            if inadimplente:
                data_pagamento_atual_str = aluno.data_pagamento.strftime('%d/%m/%Y') if aluno.data_pagamento else 'N/A'
                inadimplentes.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'dataPagamento': data_pagamento_atual_str
                })
            
            if aluno.data_atualizacao:
                # Calcular a data limite para a próxima atualização de medidas (60 dias após a última atualização)
                data_limite_atualizacao = aluno.data_atualizacao + timedelta(days=60)
                
                # Calcular a data atual mais 6 dias
                data_limite_seis_dias = datetime.now() + timedelta(days=6)

                # Verificar se a data limite está dentro dos próximos 6 dias
                if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
                    alunos_atualizar_medidas.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'ultimaAtualizacaoMedidas': aluno.data_atualizacao.strftime('%d/%m/%Y'),
                        'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y')
                    })
            else:
                # Se a data de atualização estiver faltando, adicione o aluno à lista com a indicação para atualizar
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': 'Atualizar medidas'
                })
        quantidade_alunos = len(alunos)
    return render_template("pages/adm/home/index.jinja",total_alunos_ativos=total_alunos_ativos, alunos=alunos, alunos_atualizar_medidas=alunos_atualizar_medidas, alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, quantidade_alunos=quantidade_alunos, manifest=manifest)


# Tela inadimpletes do app
@initial_app.route("/inadimplentes", methods=["GET", "POST"])
@admin_required
def inadimplentes():
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)

        alunos_pagam_semana = []
        inadimplentes = []
        alunos_atualizar_medidas = []
        total_alunos_ativos = 0
        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente
            
            if not inadimplente:
                total_alunos_ativos += 1

            if proxima_data_pagamento:
                # Converta proxima_data_pagamento para datetime para comparação
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                data_limite = datetime.now() + timedelta(days=6)
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            if inadimplente:
                data_pagamento_atual_str = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                inadimplentes.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'dataPagamento': data_pagamento_atual_str
                })

            if aluno.data_atualizacao:
                # Calcular a data limite para a próxima atualização de medidas (60 dias após a última atualização)
                data_limite_atualizacao = aluno.data_atualizacao + timedelta(days=60)
                
                # Calcular a data atual mais 6 dias
                data_limite_seis_dias = datetime.now() + timedelta(days=6)

                # Verificar se a data limite está dentro dos próximos 6 dias
                if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
                    alunos_atualizar_medidas.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'ultimaAtualizacaoMedidas': aluno.data_atualizacao.strftime('%d/%m/%Y'),
                        'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y')
                    })
            else:
                # Se a data de atualização estiver faltando, adicione o aluno à lista com a indicação para atualizar
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': 'Atualizar medidas'
                })
                
        quantidade_alunos = len(alunos)
    return render_template("pages/adm/home/inadimplentes.jinja",total_alunos_ativos=total_alunos_ativos, alunos=alunos, alunos_atualizar_medidas=alunos_atualizar_medidas, alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, quantidade_alunos=quantidade_alunos, manifest=manifest)


# Tela pagantes da semana
@initial_app.route("/pagamsemana", methods=["GET", "POST"])
@admin_required
def pagamsemana():
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)

        alunos_pagam_semana = []
        inadimplentes = []
        alunos_atualizar_medidas = []
        total_alunos_ativos = 0
        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente
            
            if not inadimplente:
                total_alunos_ativos += 1

            if proxima_data_pagamento:
                # Converta proxima_data_pagamento para datetime para comparação
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                data_limite = datetime.now() + timedelta(days=6)
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            if inadimplente:
                data_pagamento_atual_str = aluno.data_pagamento.strftime('%d/%m/%Y') if aluno.data_pagamento else 'N/A'
                inadimplentes.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'dataPagamento': data_pagamento_atual_str
                })

            if aluno.data_atualizacao:
                # Calcular a data limite para a próxima atualização de medidas (60 dias após a última atualização)
                data_limite_atualizacao = aluno.data_atualizacao + timedelta(days=60)
                
                # Calcular a data atual mais 6 dias
                data_limite_seis_dias = datetime.now() + timedelta(days=6)

                # Verificar se a data limite está dentro dos próximos 6 dias
                if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
                    alunos_atualizar_medidas.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'ultimaAtualizacaoMedidas': aluno.data_atualizacao.strftime('%d/%m/%Y'),
                        'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y')
                    })
            else:
                # Se a data de atualização estiver faltando, adicione o aluno à lista com a indicação para atualizar
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': 'Atualizar medidas'
                })
        quantidade_alunos = len(alunos)
    return render_template("pages/adm/home/pagamsemana.jinja",total_alunos_ativos=total_alunos_ativos, alunos=alunos, alunos_atualizar_medidas=alunos_atualizar_medidas, alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, quantidade_alunos=quantidade_alunos, manifest=manifest)


@initial_app.route("/atualizarmedidas", methods=["GET", "POST"])
@admin_required
def atualizarmedidas():
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)

        alunos_atualizar_medidas = []
        alunos_pagam_semana = []
        inadimplentes = []
        total_alunos_ativos = 0

        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente

            if not inadimplente:
                total_alunos_ativos += 1

            if inadimplente:
                data_pagamento_atual_str = aluno.data_pagamento.strftime('%d/%m/%Y') if aluno.data_pagamento else 'N/A'
                inadimplentes.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'dataPagamento': data_pagamento_atual_str
                })

            if proxima_data_pagamento:
                # Converta proxima_data_pagamento para datetime para comparação
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                data_limite = datetime.now() + timedelta(days=6)
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            if aluno.data_atualizacao:
                # Calcular a data limite para a próxima atualização de medidas (60 dias após a última atualização)
                data_limite_atualizacao = aluno.data_atualizacao + timedelta(days=60)
                
                # Calcular a data atual mais 6 dias
                data_limite_seis_dias = datetime.now() + timedelta(days=6)

                # Verificar se a data limite está dentro dos próximos 6 dias
                if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
                    alunos_atualizar_medidas.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'ultimaAtualizacaoMedidas': aluno.data_atualizacao.strftime('%d/%m/%Y'),
                        'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y')
                    })
            else:
                # Se a data de atualização estiver faltando, adicione o aluno à lista com a indicação para atualizar
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': 'Atualizar medidas'
                })
        quantidade_alunos = len(alunos)
    return render_template("pages/adm/home/atualizarmedidas.jinja",total_alunos_ativos=total_alunos_ativos, alunos=alunos, alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, alunos_atualizar_medidas=alunos_atualizar_medidas, quantidade_alunos=quantidade_alunos, manifest=manifest)