from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import Querys



treino_app = Blueprint("treino_app", __name__, url_prefix="/treinos", template_folder='templates',static_folder='static')


@treino_app.route("/", methods=["GET", "POST"])
def mostrar():
    # Exemplo de dados dinâmicos, substitua isso pelos dados reais da sua aplicação
    dados_treino = {
        "nome_aluno": "João",
        "exercicio": "Levantamento de Peso",
        "num_series": 3,
        "num_repeticoes": 12,
        "peso": 50
    }

    return render_template("treinos_alunos.html", dados_treino=dados_treino)