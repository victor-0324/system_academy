from flask import Blueprint, request, render_template, url_for, redirect, current_app, send_file, jsonify, json
from src.database.querys import Querys
from src.database.models import Category
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
        
        for aluno in alunos:
            # Calcular a próxima data de pagamento
            data_pagamento_atual = aluno.data_pagamento.strftime('%Y-%m-%d') if aluno.data_pagamento else None
            proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
            inadimplente = aluno.inadimplente
            
            if inadimplente:
                proxima_data_pagamento_list.append(proxima_data_pagamento)

            if not inadimplente:
                total_alunos_ativos += 1

            if proxima_data_pagamento:
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

    return render_template(
        "pages/adm/home/index.jinja",
        total_alunos_ativos=total_alunos_ativos,
        alunos=alunos,
        alunos_atualizar_medidas=alunos_atualizar_medidas,
        alunosPagamSemana=alunos_pagam_semana,
        inadimplentes=inadimplentes,
        quantidade_alunos=quantidade_alunos,
        manifest=manifest
    )


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
        # Carregar o arquivo manifest.json
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)

        # Configuração de sessão e consulta ao banco
        session = current_app.db.session
        querys_instance = Querys(session)
        alunos = querys_instance.mostrar(session)

        # Inicialização das listas
        alunos_atualizar_medidas = []
        alunos_pagam_semana = []
        inadimplentes = []
        total_alunos_ativos = 0

        # Iterar sobre cada aluno
        for aluno in alunos:
            # Verificar se o aluno está inadimplente e a data de pagamento
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
                # Verificar se o pagamento está nos próximos 6 dias
                proxima_data_pagamento_dt = datetime.strptime(proxima_data_pagamento, '%d/%m/%Y')
                data_limite = datetime.now() + timedelta(days=6)
                if proxima_data_pagamento_dt <= data_limite and not inadimplente:
                    alunos_pagam_semana.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'proximaDataPagamento': proxima_data_pagamento
                    })

            # Verificar a atualização de medidas
            precisa_atualizar_medidas = False
            precisa_atualizar_exercicios = False
            mensagem = ''

            if aluno.data_atualizacao:
                # Calcular a data limite para a próxima atualização de medidas (60 dias após a última atualização)
                data_limite_atualizacao = aluno.data_atualizacao + timedelta(days=60)
                
                # Calcular a data atual mais 6 dias
                data_limite_seis_dias = datetime.now() + timedelta(days=6)

                # Verificar se as medidas precisam ser atualizadas nos próximos 6 dias
                if datetime.now() <= data_limite_atualizacao <= data_limite_seis_dias and not inadimplente:
                    precisa_atualizar_medidas = True
                    mensagem = 'Prox, Atualização.'
                    alunos_atualizar_medidas.append({
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'ultimaAtualizacaoMedidas': aluno.data_atualizacao.strftime('%d/%m/%Y'),
                        'dataLimiteAtualizacao': data_limite_atualizacao.strftime('%d/%m/%Y'),
                        'mensagem': mensagem
                    })
            else:
                # Se não houver uma data de atualização, marcar como precisando de atualização de medidas
                mensagem = 'Sem Data De Atualização.'
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': mensagem
                })

            # Verificar se os exercícios precisam ser atualizados (lógica simplificada)
            for exercicio in aluno.exercicios:
                data_atualizacao_exercicio = exercicio.atualizacao
                if data_atualizacao_exercicio:
                    data_limite_exercicio = data_atualizacao_exercicio + timedelta(days=60)
                    if datetime.now() <= data_limite_exercicio <= datetime.now() + timedelta(days=6):
                        precisa_atualizar_exercicios = True
                        mensagem = 'Atualizar os exercícios.'
                        break  # Parar de verificar outros exercícios

            # Adicionar à lista se precisa atualizar medidas ou exercícios
            if precisa_atualizar_medidas and precisa_atualizar_exercicios:
                mensagem = 'Atualizar Exercicios & Medidas'
                alunos_atualizar_medidas.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'mensagem': mensagem
                })

          

        quantidade_alunos = len(alunos)

    return render_template(
        "pages/adm/home/atualizarmedidas.jinja",
        total_alunos_ativos=total_alunos_ativos,
        alunos=alunos,
        alunosPagamSemana=alunos_pagam_semana,
        inadimplentes=inadimplentes,
        alunos_atualizar_medidas=alunos_atualizar_medidas,
        quantidade_alunos=quantidade_alunos,
        manifest=manifest
    )


# cadastrar categoria
@initial_app.route("/categorias", methods=["GET", "POST"])
@admin_required
def categorias():
    if request.method == "POST":
        data = request.get_json()  # Recebe os dados JSON
        categoria_nome = data['categoria']
      
        # Iniciar sessão do banco de dados
        session = current_app.db.session
        querys_instance = Querys(session)
      
        # Chamar a função para adicionar a categoria e os exercícios
        querys_instance.adicionar_categoria_e_exercicios(categoria_nome, data['exercicios'])

        # Redirecionar ou retornar uma resposta adequada
        return redirect(url_for('initial_app.categorias'))
    
    session = current_app.db.session
    querys_instance = Querys(session)
    
    categorias = querys_instance.obter_categorias()
    with current_app.app_context():
        with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)
      
    return render_template("pages/adm/categorias/index.jinja",categorias=categorias, manifest=manifest)


@initial_app.route("/categorias/exercicios/<int:categoria_id>", methods=["GET", "POST"])
@admin_required
def categorias_exercicio(categoria_id):
    session = current_app.db.session
    querys_instance = Querys(session)
    
    if request.method == "POST":
        # Recebe o JSON com o ID da categoria
        data = request.get_json()
        categoria_id = data.get('categoria')
        
        # Verifica se o ID foi fornecido
        if not categoria_id:
            return jsonify({"error": "ID da categoria não fornecido"}), 400
        
        # Busca exercícios da categoria
        exercicios = querys_instance.obter_exercicios_por_categoria(categoria_id)
        
        # Retorna os exercícios no formato JSON
        return jsonify(exercicios=[exercicio.to_dict() for exercicio in exercicios])

    # Para o GET, busca a categoria e os exercícios associados
    categoria = querys_instance.obter_categoria_por_id(categoria_id)
    exercicios = querys_instance.obter_exercicios_por_categoria(categoria_id)    # Verifica se a categoria foi encontrada
    if not categoria:
        return "Categoria não encontrada", 404

    # Carrega o manifest (opcional)
    with open('src/static/manifest.json', 'r') as file:
        manifest = json.load(file)
      
    return render_template("pages/adm/categorias/exercicios/exercicios.jinja",categoria_id=categoria_id, categoria=categoria, exercicios=exercicios, manifest=manifest)


@initial_app.route("/categoria/deletar/<int:categoria_id>",methods=["POST"])
@admin_required
def deletar_categoria(categoria_id):
    try:
        session = current_app.db.session
        # Crie uma instância da classe Querys
        querys_instance = Querys(session)

        # Chame o método deletar_categoria na instância
        categoria_excluida = querys_instance.deletar_categoria(categoria_id)

        if categoria_excluida:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Categoria não encontrada'}), 404

    except Exception as e:
        print(f'Erro ao excluir categoria: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500

@initial_app.route('/categoria/exercicio/editar/<int:exercicio_id>', methods=['POST'])
@admin_required
def editar_exercicio(exercicio_id):
    session = current_app.db.session
        # Crie uma instância da classe Querys
    querys_instance = Querys(session)
    dados = request.get_json()  # Obtém os dados enviados via AJAX

    sucesso, mensagem = querys_instance.editar_exercicio_cat(exercicio_id, dados)

    if sucesso:
        return jsonify({'message': mensagem}), 200
    else:
        return jsonify({'message': mensagem}), 404
    

@initial_app.route("/categoria/exercicio/deletar/<int:exercicio_id>",  methods=['DELETE'])
@admin_required
def deletar_exercicio(exercicio_id):
    try:
        session = current_app.db.session
        # Crie uma instância da classe Querys
        querys_instance = Querys(session)

        # Chame o método deletar_exercicio na instância
        exercicio_excluida = querys_instance.deletar_exercicio_cat(exercicio_id)

        if exercicio_excluida:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'exercicio não encontrada'}), 404

    except Exception as e:
        print(f'Erro ao excluir exercicio: {str(e)}')
        return jsonify({'error': 'Erro no servidor'}), 500


@initial_app.route('/categoria/adicionar/exercicio', methods=['POST'])
@admin_required
def adicionar_exercicio():
    try:
        session = current_app.db.session
        querys_instance = Querys(session)
        dados = request.get_json()  # Obtém os dados enviados via AJAX

        categoria_id = dados.get('categoria')
        novo_nome_categoria = dados.get('categoriaName')
        
        # Obtém o nome atual da categoria
        categoria_atual = querys_instance.obter_categoria_por_id(categoria_id)

        if categoria_atual:
            # Verifica se o nome atual é diferente do novo nome
            if categoria_atual != novo_nome_categoria:
                # Atualiza o nome da categoria
                categoria = session.query(Category).filter_by(id=categoria_id).one_or_none()
                if categoria:
                    categoria.name = novo_nome_categoria
                    session.commit()
        
        # Adicionar os exercícios
        sucesso, mensagem = querys_instance.adicionar_exercicio(dados)
        
        if sucesso:
            return jsonify({'message': mensagem}), 201
        else:
            return jsonify({'message': mensagem}), 400

    except Exception as e:
        print(f'Erro ao adicionar exercício: {str(e)}')
        return jsonify({'message': 'Erro no servidor'}), 500
    

@initial_app.route("/busca_exercicios", methods=["GET", "POST"])
@admin_required
def busca_exercicios():
    if request.method == "POST":
        data = request.get_json()  # Recebe os dados JSON
        
        # Iniciar sessão do banco de dados
        session = current_app.db.session
        querys_instance = Querys(session)
        # Extrair o nome do aluno e o filtro de dias
        nome_aluno = data.get('alunoName')
        filtro_dias = data.get('searchOptions')
        categoriaId = data.get('categoriaId')
      
        # Chamar a função para busca os exercicios de um aluno
        exercicio_aluno = querys_instance.atualizar_exercicios_cat( nome_aluno, filtro_dias, categoriaId )

        
        if exercicio_aluno:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'exercicio não encontrada'}), 404
    

