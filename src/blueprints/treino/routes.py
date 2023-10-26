from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import Querys



treino_app = Blueprint("treino_app", __name__, url_prefix="/treinos", template_folder='templates',static_folder='static')


@treino_app.route("/", methods=["GET", "POST"])
def mostrar():
    # Exemplo de dados dinâmicos, substitua isso pelos dados reais da sua aplicação
    dados_treino = {
         'segunda e sexta': [
                    {
                        'nome': 'Bicicleta',
                        'serie': 1,
                        'repeticao': '3 minutos',
                        'tempoDescanso': '40 seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Crucifixo Baixo Halter',
                        'serie': 3,
                        'repeticao': 'Falha',
                        'tempoDescanso': '45 seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Supino Inclinado ($5/F5)',
                        'serie': 3,
                        'repeticao': 'Falha',
                        'tempoDescanso': '45 seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Crucifixo Reto',
                        'serie': 4,
                        'repeticao': 'Falha',
                        'tempoDescanso': '45 Seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Triceps Banco',
                        'serie': 2,
                        'repeticao': 'Restpause',
                        'tempoDescanso': '45 seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Francês Barra H',
                        'serie': 4,
                        'repeticao': '12',
                        'tempoDescanso': '45 seg',
                        'carga': 'Constante'
                    },
                    {
                        'nome': 'Triceps Unilateral Cross',
                        'serie': 5,
                        'repeticao': 'Falha',
                        'tempoDescanso': 'S/D',
                        'carga': 'Constante'
                    }
                ],
    }

    return render_template("treinos_alunos.html", dados_treino=dados_treino) 

