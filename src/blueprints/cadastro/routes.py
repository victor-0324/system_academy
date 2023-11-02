from flask import Blueprint, request, render_template, url_for, redirect, jsonify
from src.database.querys import  Querys
import json

cadastro_app = Blueprint("cadastro_app", __name__, url_prefix="/cadastro", template_folder='templates',static_folder='static')

# Tela Iniciarl do app
@cadastro_app.route("/", methods=["GET", "POST"])
def cadastrar():
    if request.method == 'POST':
        try:
            print(f'Recebendo dados: {request.form}')
            
            data = request.form.get('exercicios')
            exercicios = json.loads(data) if data else []
            
            nome = request.form.get('nome')
            idade = request.form.get('idade')
            sexo = request.form.get('sexo')
            altura = request.form.get('altura')
            peso = request.form.get('peso')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            login = request.form.get('login')
            senha = request.form.get('senha')
            dia_semana = request.form.get('dia_semana')
            horario = request.form.get('horario')
            inicio = request.form.get('inicio')
            obj = request.form.get('obj')
            
           
            # Chame a função para cadastrar o aluno no banco de dados
            Querys.cadastrar_aluno(
                nome, idade, sexo, altura, peso, email, telefone,
                login, senha, dia_semana, horario, inicio, obj,
                exercicios
            )

            return jsonify({'success': True}), 200

        except Exception as e:
            print(f'Erro no servidor: {str(e)}')
            return jsonify({'error': 'Erro no servidor'}), 500

    return render_template("cadastro.html")

  