from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    current_app,
    abort,
    json,
    jsonify,
    request,
    flash,
)
from flask_login import current_user
from src.database.querys import Querys
from functools import wraps
from src.database.models import Aluno
from zoneinfo import ZoneInfo

# from .consultas import ConsultaTreino
from datetime import datetime, timedelta

treino_app = Blueprint(
    "treino_app",
    __name__,
    url_prefix="/treino",
    template_folder="templates",
    static_folder="static",
)


def formatar_data(data):
    if data is None:
        return "Inicio Da Evolução"
    return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")


def treino_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'treino' e que não estão inadimplentes."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            current_user.is_authenticated
            and current_user.permissao == "treino"
            and not current_user.inadimplente
        ):
            return func(*args, **kwargs)
        else:

            return redirect(url_for("login_app.login"))

    return wrapper


def calcular_proxima_data_pagamento(data_pagamento_atual):
    if data_pagamento_atual:
        # Converter a string da data de pagamento atual para um objeto datetime
        data_pagamento_atual = datetime.strptime(data_pagamento_atual, "%Y-%m-%d")

        # Calcular a próxima data de pagamento com base em 30 dias de inadimplência
        proxima_data_pagamento = data_pagamento_atual + timedelta(days=30)

        # Verificar se o mês atual tem mais de 30 dias e adicionar um dia extra se necessário
        if data_pagamento_atual.month == proxima_data_pagamento.month:
            proxima_data_pagamento += timedelta(days=1)

        # Formatando a próxima data de pagamento como string
        proxima_data_pagamento_str = proxima_data_pagamento.strftime("%d/%m/%Y")
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
    data_pagamento_atual = (
        aluno.data_pagamento.strftime("%Y-%m-%d") if aluno.data_pagamento else None
    )
    proxima_data_pagamento = calcular_proxima_data_pagamento(data_pagamento_atual)
    with open("src/static/manifest.json", "r") as file:
        manifest = json.load(file)

    # Verificação de pagamento
    faltam_tres_dias = querys_instance.verificar_falta_tres_dias(aluno_id)
    return render_template(
        "aluno_treino.html",
        proxima_data_pagamento=proxima_data_pagamento,
        exercicios=exercicios,
        faltam_tres_dias=faltam_tres_dias,
        aluno=aluno,
        manifest=manifest,
    )


@treino_app.route("/evolucao/<int:aluno_id>", methods=["GET"])
@treino_required
def evolucao(aluno_id):
    with current_app.app_context():
        with open("src/static/manifest.json", "r") as file:
            manifest = json.load(file)

    session = current_app.db.session
    querys_instance = Querys(session)
    aluno = querys_instance.session.query(Aluno).filter_by(id=aluno_id).first()

    if aluno:
        medidas = querys_instance.get_medidas_por_aluno(aluno_id)

        # Verificar se as medidas foram carregadas
        if not medidas:
            return render_template(
                "evolucao.html", aluno=aluno, manifest=manifest, medidas=[]
            )

        # Garantir que todos os valores de data_atualizacao são do tipo datetime
        for medida in medidas:
            if medida["data_atualizacao"] is not None:
                if isinstance(medida["data_atualizacao"], str):
                    medida["data_atualizacao"] = datetime.strptime(
                        medida["data_atualizacao"], "%Y-%m-%d %H:%M:%S"
                    )
                elif not isinstance(medida["data_atualizacao"], datetime):
                    medida["data_atualizacao"] = datetime.fromtimestamp(
                        medida["data_atualizacao"]
                    )

        # Filtrar medidas onde data_atualizacao não é None
        medidas = [m for m in medidas if m["data_atualizacao"] is not None]

        # Ordenar por data
        medidas.sort(
            key=lambda x: x["data_atualizacao"], reverse=True
        )  # Ordenar do mais recente para o mais antigo

        return render_template(
            "evolucao.html", aluno=aluno, medidas=medidas, manifest=manifest
        )
    else:
        abort(404)


treinos = {}
@treino_required
@treino_app.route("/iniciar_treino", methods=["POST"])
def iniciar_treino():
    dados = request.json
    aluno_id = dados.get("aluno_id")

    if not aluno_id:
        return jsonify({"error": "ID do aluno é obrigatório"}), 400

    inicio_treino  = datetime.now(ZoneInfo("America/Sao_Paulo"))
    print(f"Iniciando treino para o aluno {aluno_id} às {inicio_treino}")
    # Salva temporariamente na memória
    treinos[aluno_id] = {"inicio": inicio_treino, "status": "em andamento"}

    return jsonify({"status": "sucesso", "inicio": inicio_treino.isoformat()})


@treino_required
@treino_app.route("/finalizar_treino", methods=["POST"])
def finalizar_treino():
    dados = request.json
    aluno_id = dados.get("aluno_id")
    tempo_inicial = dados.get("tempo_inicial")
    session = current_app.db.session
    querys_instance = Querys(session)

    if not aluno_id or not tempo_inicial:
        return jsonify({"error": "Dados inválidos"}), 400

    fuso_brasilia = ZoneInfo("America/Sao_Paulo")

    agora = datetime.now(fuso_brasilia)
    inicio = datetime.fromtimestamp(int(tempo_inicial) / 1000, tz=fuso_brasilia)

    duracao = agora - inicio

    if duracao < timedelta(minutes=1):
        return jsonify({"error": "Tempo de treino muito curto para pontuar."}), 400

    pontos = querys_instance.calcular_pontos(duracao)

    resultado = querys_instance.salvar_progresso(aluno_id, duracao, pontos)
    if resultado is False:
        flash("Progresso não foi salvo porque hoje é domingo.", "warning")

    return jsonify({"status": "sucesso", "duracao": str(duracao), "pontos": pontos})


@treino_required
@treino_app.route("/verificar_progresso_semanal", methods=["GET"])
def verificar_progresso_semanal():
    aluno_id = request.args.get("aluno_id")
    if not aluno_id:
        return jsonify({"error": "ID do aluno é obrigatório"}), 400

    session = current_app.db.session
    querys_instance = Querys(session)

    registros = querys_instance.busca_progresso_semanal(aluno_id)
    if not registros:
        return jsonify({"error": "Nenhum progresso encontrado"}), 404

    fuso_brasilia = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia)
    inicio_semana = (agora - timedelta(days=agora.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    mapa = {}
    pontos_contabilizados = set()
    for p in sorted(registros, key=lambda r: getattr(r, "data_criacao", datetime.now(fuso_brasilia))):
        dt = getattr(p, "data_criacao", None)
        if dt is None:
            dt = datetime.now(fuso_brasilia)
        elif dt.tzinfo is None:
            dt = dt.replace(tzinfo=fuso_brasilia)

        if dt < inicio_semana:
            continue

        key = dt.date().isoformat()

        if key not in mapa:
            mapa[key] = {"tempo": 0, "pontos": 0}

        tempo = p.tempo_treino.total_seconds() if isinstance(p.tempo_treino, timedelta) else 0
        mapa[key]["tempo"] += tempo

        if key not in pontos_contabilizados:
            mapa[key]["pontos"] += getattr(p, "pontos", 0)
            pontos_contabilizados.add(key)

    nomes_pt = {
        0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
        3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo",
    }

    progresso = []
    total_pontos = 0
    hoje_date = agora.date()

    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        chave = dia.date().isoformat()
        dia_nome = nomes_pt[dia.weekday()]

        if dia.date() < hoje_date:
            status = "✅" if chave in mapa else "❌"
        elif dia.date() == hoje_date:
            status = "✅" if chave in mapa else ""
        else:
            status = ""

        tempo = mapa.get(chave, {}).get("tempo", 0)
        pontos = mapa.get(chave, {}).get("pontos", 0)
        total_pontos += pontos

        progresso.append({
            "data": chave,
            "dia_nome": dia_nome,
            "status": status,
            "tempo_treino": tempo,
            "pontos": pontos,
        })

    # 🎯 Novas funcionalidades de gamificação:
    nivel = querys_instance.calcular_nivel(aluno_id)
    conquistas = querys_instance.calcular_conquista(mapa)

    return jsonify({
        "total_pontos": total_pontos,
        "nivel": nivel,
        "conquistas": conquistas,
        "progresso": progresso
    })
