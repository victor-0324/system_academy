from flask import Blueprint, request, render_template, url_for, redirect, jsonify, current_app
from src.database.querys import  Querys
import json
from src.database.config import db_connector, DBConnectionHandler
from functools import wraps
from flask_login import current_user


cadastro_app = Blueprint("cadastro_app", __name__, url_prefix="/cadastro", template_folder='templates',static_folder='static')

def admin_required(func):
    """Decorator para restringir o acesso apenas a usuários com permissão 'admin'."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.permissao == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_app.login'))
    return wrapper


# Tela Iniciarl do app
@cadastro_app.route("/", methods=["GET", "POST"])
@admin_required
def cadastrar():
    with open('src/static/manifest.json', 'r') as file:
            manifest = json.load(file)
    if request.method == 'POST':
        try:
            data = request.form.get('exercicios')
            exercicios = json.loads(data) if data else []
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            sexo = request.form.get('sexo')
            peso = request.form.get('peso')
            ombro = request.form.get('ombro')
            torax = request.form.get('torax')
            braco_d = request.form.get('braco_d')
            braco_e = request.form.get('braco_e')
            ant_d = request.form.get('ant_d')
            ant_e = request.form.get('ant_e')
            cintura = request.form.get('cintura')
            abdome = request.form.get('abdome')
            quadril = request.form.get('quadril')
            coxa_d = request.form.get('coxa_d')
            coxa_e = request.form.get('coxa_e')
            pant_d = request.form.get('pant_d')
            pant_e = request.form.get('pant_e')
            observacao = request.form.get('observacao')
            telefone = request.form.get('telefone')
            login = request.form.get('login')
            senha = request.form.get('senha')
            data_entrada = request.form.get('data_entrada')
            data_pagamento = request.form.get('data_pagamento')
            jatreino = request.form.get('jatreino')
            permissao = request.form.get('permissao')

            session = current_app.db.session
            # Crie uma instância da classe Querys
            querys_instance = Querys(session)
            
            # Chame o método cadastrar_aluno na instância
            querys_instance.cadastrar_aluno(
                nome, idade, sexo, peso, ombro, torax, braco_d, braco_e, ant_d, ant_e, cintura,
                abdome, quadril, coxa_d, coxa_e, pant_d, pant_e, observacao, telefone, login, senha,
                data_entrada, data_pagamento, jatreino, permissao,
                exercicios
            )

            return jsonify({'success': True}), 200

        except Exception as e:
            print(f'Erro no servidor: {str(e)}')
            return jsonify({'error': 'Erro no servidor'}), 500

    return render_template("cadastro.html",manifest=manifest)


@cadastro_app.route("/busca_pornome", methods=["POST"])
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

   