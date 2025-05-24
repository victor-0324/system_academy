from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    redirect,
    current_app,
    send_file,
    jsonify,
    json,
)
from src.database.querys import Querys
from src.database.models import Category
from functools import wraps
from flask_login import current_user
from .consultas import obter_dados_alunos, carregar_manifesto, obter_dados_alunos

# from dateutil.relativedelta import relativedelta

initial_app = Blueprint(
    "initial_app",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
)


@initial_app.route("/sw.js")
def serve_sw():
    return send_file("static/sw.js", mimetype="application/javascript")


@initial_app.route("/manifest.json")
def serve_manifest():
    return send_file("static/manifest.json", mimetype="application/manifest+json")


# @initial_app.route('/offline')
# def offline():
#     return jsonify({"response": 0})


@initial_app.route("/app")
def index1():
    with open("src/static/manifest.json", "r") as file:
        manifest = json.load(file)
    return render_template("index1.html", manifest=manifest)


@initial_app.route("/manifest.json")
def admin_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'admin'."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.permissao == "admin":
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login_app.login"))

    return wrapper


# Tela Iniciarl do app
@initial_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    """Tela principal do sistema"""
    manifest = carregar_manifesto()
    session = current_app.db.session
    querys_instance = Querys(session)
    alunos = querys_instance.mostrar(session)
    querys_instance.limpar_alunos()
    dados_alunos = obter_dados_alunos(alunos)
    quantidade_alunos = len(alunos)

    return render_template(
        "pages/adm/home/index.jinja",
        manifest=manifest,
        alunos=alunos,
        quantidade_alunos=quantidade_alunos,
        **dados_alunos,
    )


@initial_app.route("/inadimplentes", methods=["GET"])
@admin_required
def inadimplentes():
    manifest = carregar_manifesto()
    session = current_app.db.session
    querys_instance = Querys(session)
    alunos = querys_instance.mostrar(session)
    dados_alunos = obter_dados_alunos(alunos)
    # total_alunos_ativos, alunos_pagam_semana, inadimplentes, alunos_atualizar_medidas = obter_dados_alunos(alunos)
    quantidade_alunos = len(alunos)
    # print(total_alunos_ativos)
    return render_template(
        "pages/adm/home/inadimplentes.jinja",
        quantidade_alunos=quantidade_alunos,
        manifest=manifest,
        **dados_alunos,
    )


@initial_app.route("/pagamsemana", methods=["GET"])
@admin_required
def pagamsemana():
    manifest = carregar_manifesto()
    session = current_app.db.session
    querys_instance = Querys(session)
    alunos = querys_instance.mostrar(session)

    dados_alunos = obter_dados_alunos(alunos)
    quantidade_alunos = len(alunos)

    return render_template(
        "pages/adm/home/pagamsemana.jinja",
        quantidade_alunos=quantidade_alunos,
        manifest=manifest,
        **dados_alunos,
    )


@initial_app.route("/atualizarmedidas", methods=["GET"])
@admin_required
def atualizarmedidas():
    manifest = carregar_manifesto()
    session = current_app.db.session
    querys_instance = Querys(session)
    alunos = querys_instance.mostrar(session)

    dados_alunos = obter_dados_alunos(alunos)
    quantidade_alunos = len(alunos)

    return render_template(
        "pages/adm/home/atualizarmedidas.jinja",
        **dados_alunos,
        quantidade_alunos=quantidade_alunos,
        manifest=manifest,
    )


# cadastrar categoria
@initial_app.route("/categorias", methods=["GET", "POST"])
@admin_required
def categorias():
    if request.method == "POST":
        data = request.get_json()  # Recebe os dados JSON
        categoria_nome = data["categoria"]

        # Iniciar sessão do banco de dados
        session = current_app.db.session
        querys_instance = Querys(session)

        # Chamar a função para adicionar a categoria e os exercícios
        querys_instance.adicionar_categoria_e_exercicios(
            categoria_nome, data["exercicios"]
        )

        # Redirecionar ou retornar uma resposta adequada
        return redirect(url_for("initial_app.categorias"))

    session = current_app.db.session
    querys_instance = Querys(session)

    categorias = querys_instance.obter_categorias()
    with current_app.app_context():
        with open("src/static/manifest.json", "r") as file:
            manifest = json.load(file)

    return render_template(
        "pages/adm/categorias/index.jinja", categorias=categorias, manifest=manifest
    )


@initial_app.route("/categorias/exercicios/<int:categoria_id>", methods=["GET", "POST"])
@admin_required
def categorias_exercicio(categoria_id):
    session = current_app.db.session
    querys_instance = Querys(session)

    if request.method == "POST":
        # Recebe o JSON com o ID da categoria
        data = request.get_json()
        categoria_id = data.get("categoria")

        # Verifica se o ID foi fornecido
        if not categoria_id:
            return jsonify({"error": "ID da categoria não fornecido"}), 400

        # Busca exercícios da categoria
        exercicios = querys_instance.obter_exercicios_por_categoria(categoria_id)

        # Retorna os exercícios no formato JSON
        return jsonify(exercicios=[exercicio.to_dict() for exercicio in exercicios])

    # Para o GET, busca a categoria e os exercícios associados
    categoria = querys_instance.obter_categoria_por_id(categoria_id)
    exercicios = querys_instance.obter_exercicios_por_categoria(
        categoria_id
    )  # Verifica se a categoria foi encontrada
    if not categoria:
        return "Categoria não encontrada", 404

    # Carrega o manifest (opcional)
    with open("src/static/manifest.json", "r") as file:
        manifest = json.load(file)

    return render_template(
        "pages/adm/categorias/exercicios/exercicios.jinja",
        categoria_id=categoria_id,
        categoria=categoria,
        exercicios=exercicios,
        manifest=manifest,
    )


@initial_app.route("/categoria/deletar/<int:categoria_id>", methods=["POST"])
@admin_required
def deletar_categoria(categoria_id):
    try:
        session = current_app.db.session
        # Crie uma instância da classe Querys
        querys_instance = Querys(session)

        # Chame o método deletar_categoria na instância
        categoria_excluida = querys_instance.deletar_categoria(categoria_id)

        if categoria_excluida:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Categoria não encontrada"}), 404

    except Exception as e:
        print(f"Erro ao excluir categoria: {str(e)}")
        return jsonify({"error": "Erro no servidor"}), 500


@initial_app.route("/categoria/exercicio/editar/<int:exercicio_id>", methods=["POST"])
@admin_required
def editar_exercicio(exercicio_id):
    session = current_app.db.session
    # Crie uma instância da classe Querys
    querys_instance = Querys(session)
    dados = request.get_json()  # Obtém os dados enviados via AJAX

    sucesso, mensagem = querys_instance.editar_exercicio_cat(exercicio_id, dados)

    if sucesso:
        return jsonify({"message": mensagem}), 200
    else:
        return jsonify({"message": mensagem}), 404


@initial_app.route(
    "/categoria/exercicio/deletar/<int:exercicio_id>", methods=["DELETE"]
)
@admin_required
def deletar_exercicio(exercicio_id):
    try:
        session = current_app.db.session
        # Crie uma instância da classe Querys
        querys_instance = Querys(session)

        # Chame o método deletar_exercicio na instância
        exercicio_excluida = querys_instance.deletar_exercicio_cat(exercicio_id)

        if exercicio_excluida:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "exercicio não encontrada"}), 404

    except Exception as e:
        print(f"Erro ao excluir exercicio: {str(e)}")
        return jsonify({"error": "Erro no servidor"}), 500


@initial_app.route("/categoria/adicionar/exercicio", methods=["POST"])
@admin_required
def adicionar_exercicio():
    try:
        session = current_app.db.session
        querys_instance = Querys(session)
        dados = request.get_json()  # Obtém os dados enviados via AJAX

        categoria_id = dados.get("categoria")
        novo_nome_categoria = dados.get("categoriaName")

        # Obtém o nome atual da categoria
        categoria_atual = querys_instance.obter_categoria_por_id(categoria_id)

        if categoria_atual:
            # Verifica se o nome atual é diferente do novo nome
            if categoria_atual != novo_nome_categoria:
                # Atualiza o nome da categoria
                categoria = (
                    session.query(Category).filter_by(id=categoria_id).one_or_none()
                )
                if categoria:
                    categoria.name = novo_nome_categoria
                    session.commit()

        # Adicionar os exercícios
        sucesso, mensagem = querys_instance.adicionar_exercicio(dados)

        if sucesso:
            return jsonify({"message": mensagem}), 201
        else:
            return jsonify({"message": mensagem}), 400

    except Exception as e:
        print(f"Erro ao adicionar exercício: {str(e)}")
        return jsonify({"message": "Erro no servidor"}), 500


@initial_app.route("/busca_exercicios", methods=["GET", "POST"])
@admin_required
def busca_exercicios():
    if request.method == "POST":
        data = request.get_json()  # Recebe os dados JSON

        # Iniciar sessão do banco de dados
        session = current_app.db.session
        querys_instance = Querys(session)
        # Extrair o nome do aluno e o filtro de dias
        nome_aluno = data.get("alunoName")
        filtro_dias = data.get("searchOptions")
        categoriaId = data.get("categoriaId")

        # Chamar a função para busca os exercicios de um aluno
        exercicio_aluno = querys_instance.atualizar_exercicios_cat(
            nome_aluno, filtro_dias, categoriaId
        )

        if exercicio_aluno:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "exercicio não encontrada"}), 404


@initial_app.route("/uploadImg", methods=["GET", "POST"])
@admin_required
def uploadIm():
    pass
