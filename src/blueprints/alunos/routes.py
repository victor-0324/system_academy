from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import Querys
from datetime import datetime
from src.database.config import db, db_connector, DBConnectionHandler
from flask_login import current_user, login_required
from functools import wraps
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 
import json
from copy import deepcopy 
from .exercicios import ExerciciosView

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

# Tela Iniciarl do app
@clientes_app.route("/", methods=["GET", "POST"])
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

        # Iterar sobre cada aluno na lista
        for aluno in alunos:
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente
            
            if inadimplente:
                proxima_data_pagamento_list.append(proxima_data_pagamento)

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
        quantidade_alunos = len(alunos)
    return render_template("pages/adm/home/index.jinja", alunos=alunos, alunosPagamSemana=alunos_pagam_semana, inadimplentes=inadimplentes, quantidade_alunos=quantidade_alunos, manifest=manifest, proxima_data_pagamento_list=proxima_data_pagamento_list)

@clientes_app.route("/detalhes/<int:aluno_id>", methods=["GET"])
@admin_required
def mostrar_detalhes(aluno_id):
    with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        aluno = querys_instance.mostrar_detalhes(aluno_id) 
        
        # Obter apenas a data de pagamento do aluno
        data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
        # Calcular a próxima data de pagamento
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            
        # Verificar se o aluno é inadimplente
        inadimplente = aluno.inadimplente
    return render_template("pages/alunos/detalhes/index.jinja", aluno=[aluno], inadimplente=inadimplente, proxima_data_pagamento=proxima_data_pagamento, data_pagamento_atual=data_pagamento_atual, manifest=manifest)

@clientes_app.route("/atualizar_ex/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar_ex(aluno_id):
    with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)
    session = current_app.db.session
    querys_instance = Querys(session)
    if request.method == "POST":
        data = request.form.get('exercicios')
        exercicios = json.loads(data) if data else []
        # Suponha que a função 'atualizar_exercicios' retorne uma resposta ou estado desejado
        resultado_atualizacao = querys_instance.atualizar_exercicios(aluno_id, exercicios)

        if resultado_atualizacao:  # Adapte conforme necessário
            return jsonify({'success': True, 'message': 'Exercícios atualizados com sucesso'}), 200
        else:
            return jsonify({'error': 'Falha ao atualizar exercícios'}), 500

    else:
        aluno = querys_instance.mostrar_detalhes(aluno_id)
        exercicios = querys_instance.criar_objeto_exercicio(aluno_id)
        return render_template("pages/alunos/exercicios/index.jinja", exercicios=exercicios,aluno=aluno, manifest=manifest)

@clientes_app.route("/atualizar_medidas/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar_medidas(aluno_id):
    session = current_app.db.session
    querys_instance = Querys(session)
    try:
        if request.method == "POST":
            peso = request.form.get('peso')
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
            aluno = querys_instance.mostrar_detalhes(aluno_id)

            # Use a função atualizar_dados para atualizar as informações do aluno
            aluno_antes = deepcopy(aluno)  # Crie uma cópia profunda do aluno antes da atualização
            historico_antes, historico_depois = querys_instance.atualizar_medidas(
                aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                abdome, quadril, coxa_d, coxa_e, pant_d, pant_e
            )
            
            return jsonify({'success': True, 'historico_antes': historico_antes, 'historico_depois': historico_depois}), 200
 
        else:
            aluno = querys_instance.mostrar_detalhes(aluno_id)
            return render_template("modificar.html", aluno=[aluno])

    except Exception as e:
        print(f'Erro no servidor: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500

@clientes_app.route("/atualizar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar(aluno_id):
    session = current_app.db.session
    querys_instance = Querys(session)
    try:
        if request.method == "POST":
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            observacao = request.form.get("observacao")
            telefone = request.form.get("telefone")
            login = request.form.get("login")
            senha = request.form.get("senha")
            data_pagamento = request.form.get("data_pagamento")
            permissao = request.form.get('permissao')

            aluno = querys_instance.mostrar_detalhes(aluno_id)

            # Use a função atualizar_dados para atualizar as informações do aluno
            aluno = querys_instance.atualizardados(
                aluno_id, nome, idade, observacao, telefone, login, senha, data_pagamento, permissao
            )
            
            return jsonify({'success': True}), 200
        else:
            aluno = querys_instance.mostrar_detalhes(aluno_id)
            return render_template("modificar.html", aluno=[aluno])

    except Exception as e:
        print(f'Erro no servidor: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500

@clientes_app.route("/busca_pornome", methods=["POST"])
@admin_required
def busca_pornome():
    # Certifique-se de que os dados estão sendo enviados como JSON no corpo do POST
    data = request.get_json()
    def serialize_exercicios(exercicio):
                        return {
                            'tipoTreino': exercicio.tipoTreino,
                            'exercicio': exercicio.exercicio,
                            'serie': exercicio.serie,
                            'repeticao': exercicio.repeticao,
                            'descanso': exercicio.descanso,
                            'carga': exercicio.carga,
                        }
    if 'nome_aluno' in data:
        nome_aluno = data['nome_aluno']
    
        with current_app.app_context():
            session = current_app.db.session
            querys_instance = Querys(session)
            aluno = querys_instance.buscar_exercicios_por_nome(nome_aluno)

            if aluno:
                exercicios = aluno.exercicios

                # Serializa a lista de exercícios
                exercicios_serializados = [serialize_exercicios(exercicio) for exercicio in exercicios]

               
                # Retornar os detalhes do aluno em formato JSON
                return jsonify({'status': 'success', 'aluno': {
                    'exercicios': exercicios_serializados,
                }})
            else:
                return jsonify({'status': 'error', 'message': 'Aluno não encontrado'})
    else:
        return jsonify({'status': 'error', 'message': 'Nome do aluno não fornecido no corpo do POST'})

@clientes_app.route("/deletar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def deletar(aluno_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar(aluno_id)
    return redirect(url_for("clientes_app.mostrar"))

@clientes_app.route("/deletar/exercicio/<int:exercicio_id>", methods=["GET", "POST"])
@admin_required
def deletar_ex(exercicio_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar_exercicio(exercicio_id)
    return redirect(url_for("clientes_app.mostrar"))


@clientes_app.route("/cadastrar_ex", methods=["GET", "POST"])
@admin_required
def cadastrar_ex():
    if request.method == 'POST':
        exercicio = request.get('exercicio')
        serie = request.get('serie')
        repeticao = request.get('repeticao')
        descanso = request.get('descanso')
        carga = request.get('carga')

        session = current_app.db.session
        querys_instance = Querys(session)

        querys_instance.cadastrar_ex(
                    exercicio, serie, repeticao, descanso, carga
                )
        
    return jsonify({'success': True}), 200



@clientes_app.route("/busca_adicionar/<int:aluno_id>/<string:nome_aluno>", methods=["GET", "POST"])
@admin_required
def busca_adicionar(aluno_id, nome_aluno):
    session = current_app.db.session
    querys_instance = Querys(session)

    aluno = querys_instance.buscar_exercicios_por_nome(nome_aluno)
    exercicios = querys_instance.criar_objeto_exercicio(aluno.id)
    
    # exercicios = json.dumps(exercicios_json)
   
    # Suponha que a função 'atualizar_exercicios' retorne uma resposta ou estado desejado
    resultado_atualizacao = querys_instance.atualizar_exercicios(aluno_id, exercicios)

    if resultado_atualizacao:  # Adapte conforme necessário
        return jsonify({'success': True, 'message': 'Exercícios atualizados com sucesso'}), 200
    else:
        return jsonify({'error': 'Falha ao atualizar exercícios'}), 500

    # As linhas abaixo não serão executadas se a condição acima for verdadeira
    aluno = querys_instance.mostrar_detalhes(aluno_id)
    exercicios = querys_instance.criar_objeto_exercicio(aluno_id)
    
    return render_template("pages/alunos/exercicios/index.jinja", exercicios=exercicios, aluno=aluno)

@clientes_app.route("/editar/exercicio/<int:exercicio_id>", methods=["POST"])
@admin_required
def editar_exercicio(exercicio_id):
    session = current_app.db.session
    querys_instance = Querys(session)
    try:
        if request.method == "POST":
            # Obtém os novos dados do corpo da requisição em formato JSON
            novos_dados = request.get_json()
            
            # Chama o método editar_exercicio da sua classe
            sucesso = querys_instance.editar_exercicio(exercicio_id, novos_dados)

            if sucesso:
                return jsonify({'mensagem': 'Exercício editado com sucesso'}), 200
            else:
                return jsonify({'mensagem': 'Erro ao editar exercício'}), 404

        # Se a requisição for GET, você pode renderizar um formulário de edição
        # que permitirá ao usuário fornecer os novos dados.
        else:
            # Recupera o exercício pelo id
            exercicio = querys_instance.obter_exercicio_por_id(exercicio_id)

            if exercicio:
                return render_template("formulario_edicao_exercicio.html", exercicio=exercicio)
            else:
               
                return redirect(url_for("clientes_app.mostrar"))

    except Exception as e:
        return jsonify({'mensagem': f'Erro interno: {str(e)}'}), 500


exercicio_aluno_view = ExerciciosView.as_view('exercicios_aluno_view')
clientes_app.add_url_rule('/exercicios/rest', view_func=exercicio_aluno_view)
clientes_app.add_url_rule('/exercicios/rest/<int:_id>', view_func=exercicio_aluno_view, methods=['DELETE'])