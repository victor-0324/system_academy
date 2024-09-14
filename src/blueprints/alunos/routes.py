from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import Querys
from datetime import datetime
from src.database.config import db, db_connector, DBConnectionHandler
from flask_login import current_user, login_required
from functools import wraps
from datetime import datetime, timedelta
from src.database.models import Aluno, ExerciciosAluno, Category, Exercise
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



@clientes_app.route("/detalhes/<int:aluno_id>", methods=["GET"])
@admin_required
def mostrar_detalhes(aluno_id):
    with open('src/static/manifest.json', 'r') as file:
        manifest = json.load(file)

    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        aluno = querys_instance.mostrar_detalhes(aluno_id) 
        
        if aluno.data_entrada:
            data_formatada = aluno.data_entrada.strftime('%d/%m/%Y')
        else:
            data_formatada = ''

        # Obter apenas a medida mais recente
        medida = querys_instance.get_ultima_medida(aluno_id)
        medidas = []
        
        
        if medida and medida.data_atualizacao:
            if isinstance(medida.data_atualizacao, datetime):
                # Adicionar 60 dias à data de atualização
                data_atualizacao = medida.data_atualizacao + timedelta(days=60)
                data_atualizacao_formatada = data_atualizacao.strftime('%d/%m/%Y')
            else:
                data_atualizacao_formatada = medida.data_atualizacao
        else:
            data_atualizacao_formatada = "Sem data de atualização"

        # Formatar data atual para o formato desejado
        data_atual = datetime.now().strftime('%d/%m/%Y')

        # Adicionar a medida formatada à lista de medidas
        if medida:
            medidas.append({
                'peso': medida.peso,
                'ombro': medida.ombro,
                'torax': medida.torax,
                'braco_d': medida.braco_d,
                'braco_e': medida.braco_e,
                'ant_d': medida.ant_d,
                'ant_e': medida.ant_e,
                'cintura': medida.cintura,
                'abdome': medida.abdome,
                'quadril': medida.quadril,
                'coxa_d': medida.coxa_d,
                'coxa_e': medida.coxa_e,
                'pant_d': medida.pant_d,
                'pant_e': medida.pant_e,
                'data_atualizacao': medida.data_atualizacao.strftime('%d/%m/%Y') if isinstance(medida.data_atualizacao, datetime) else medida.data_atualizacao
            })
        # Obter apenas a data de pagamento do aluno
        data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
        # Calcular a próxima data de pagamento
        proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            
        # Verificar se o aluno é inadimplente
        inadimplente = aluno.inadimplente

        if aluno.data_entrada:
            data_formatada = aluno.data_entrada.strftime('%d/%m/%Y')
        else:
            data_formatada = ''

    return render_template("pages/alunos/detalhes/index.jinja", data_atual=data_atual, aluno=aluno,data_atualizacao_formatada=data_atualizacao_formatada, data_formatada=data_formatada, inadimplente=inadimplente, proxima_data_pagamento=proxima_data_pagamento, data_pagamento_atual=data_pagamento_atual, manifest=manifest, medidas=medidas)

@clientes_app.route("/atualizar_ex/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def atualizar_ex(aluno_id):
    session = current_app.db.session
    querys_instance = Querys(session)

    if request.method == "POST":
        try:
            aluno_id = request.form.get('alunoId')
            filtro_dias = request.form.get('searchOptions')
            categoria_id = request.form.get('categoriaId')

            aluno = session.query(Aluno).filter_by(id=aluno_id).first()
            if not aluno:
                return jsonify({'error': 'Aluno não encontrado'}), 404

            nome_aluno = aluno.nome
            sucesso = querys_instance.atualizar_exercicios_aluno(nome_aluno, filtro_dias, categoria_id)

            if sucesso:
                return jsonify({'success': True, 'message': 'Exercícios atualizados com sucesso'}), 200
            else:
                return jsonify({'error': 'Falha ao atualizar exercícios'}), 500

        except Exception as e:
            print('Erro na atualização:', str(e))
            return jsonify({'error': 'Falha ao atualizar exercícios'}), 500

    else:
        aluno = session.query(Aluno).get(aluno_id)
        if not aluno:
            return render_template("pages/alunos/exercicios/index.jinja", aluno=None)

        exercicios = session.query(ExerciciosAluno).filter(ExerciciosAluno.aluno_id == aluno_id).all()
        for exercicio in exercicios:
            if exercicio.atualizacao:
                # Formata a data como 'DD/MM/YYYY HH:MM'
                exercicio.atualizacao_formatada = exercicio.atualizacao.strftime('%d/%m/%Y')
            else:
                exercicio.atualizacao_formatada = None
                
        categorias = session.query(Category).all()

        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        return render_template("pages/alunos/exercicios/index.jinja",
                               manifest=manifest,
                               exercicios=exercicios,
                               aluno=aluno,
                               categorias=categorias)
    


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
          
            # Obter as medidas antes da atualização
            historico_antes = querys_instance.get_medidas_por_aluno(aluno_id)
            
            # Atualizar as medidas
            querys_instance.atualizar_medidas(
                aluno_id, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                abdome, quadril, coxa_d, coxa_e, pant_d, pant_e
            )
            
            # Obter as medidas após a atualização
            historico_depois = querys_instance.get_medidas_por_aluno(aluno_id)
            
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
    
        return jsonify({'error': 'Erro no servidor'}), 500



@clientes_app.route("/deletar/<int:aluno_id>", methods=["GET", "POST"])
@admin_required
def deletar(aluno_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar(aluno_id)
    return redirect(url_for("initial_app.mostrar"))

@clientes_app.route("/deletar/exercicio/<int:exercicio_id>", methods=["GET", "POST"])
@admin_required
def deletar_ex(exercicio_id):
    with current_app.app_context():
        session = current_app.db.session
        querys_instance = Querys(session)
        querys_instance.deletar_exercicio(exercicio_id)
    return redirect(url_for("initial_app.mostrar"))


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



@clientes_app.route("/busca_adicionar", methods=["GET", "POST"])
@admin_required
def busca_adicionar():
    session = current_app.db.session
    querys_instance = Querys(session)
    
    if request.method == "POST":
        try:
            # Obtém os dados do corpo da requisição
            data = request.json
            aluno_name = data.get('alunoName', '')
            filtro_dias = data.get('searchOptions', 'todos')
            aluno_id = data.get('alunoId')
            
            
            # Verifica se todos os dados necessários estão presentes
            if not aluno_name or aluno_id is None:
                return jsonify({'error': 'Dados insuficientes'}), 400

            # Busca os exercícios conforme o nome e o filtro
            exercicios = querys_instance.buscar_exercicios_por_nome(aluno_name, filtro_dias)
            
            if exercicios is None:
                return jsonify({'error': 'Erro ao buscar exercícios'}), 500
            
            # Atualiza os exercícios filtrados
            sucesso_atualizacao = querys_instance.atualizar_exercicios_filtry(aluno_id, exercicios)

            if sucesso_atualizacao:
                return jsonify({'success': True, 'message': 'Exercícios atualizados com sucesso'}), 200
            else:
                return jsonify({'error': 'Falha ao atualizar exercícios'}), 500
        
        except Exception as e:
            # Registra o erro no console para depuração
            print(f"Erro: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor'}), 500

    # Retorno para requisições GET ou para outros métodos não suportados
    return jsonify({'message': 'Método não suportado'}), 405
        

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

       
        # que permitirá ao usuário fornecer os novos dados.
        else:
            # Recupera o exercício pelo id
            exercicio = querys_instance.obter_exercicio_por_id(exercicio_id)

            if exercicio:
                return render_template("formulario_edicao_exercicio.html", exercicio=exercicio)
            else:
               
                return redirect(url_for("initial_app.mostrar"))

    except Exception as e:
        return jsonify({'mensagem': f'Erro interno: {str(e)}'}), 500


exercicio_aluno_view = ExerciciosView.as_view('exercicios_aluno_view')
clientes_app.add_url_rule('/exercicios/rest', view_func=exercicio_aluno_view)
clientes_app.add_url_rule('/exercicios/rest/<int:_id>', view_func=exercicio_aluno_view, methods=['DELETE'])