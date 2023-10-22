from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import Querys

initial_app = Blueprint("initial_app", __name__, url_prefix="/", template_folder='templates',static_folder='static')

# Tela Iniciarl do app
@initial_app.route("/", methods=["GET", "POST"])
def mostrar():
    clientes = Querys.get_alunos()
    return render_template("index.html",clientes=clientes)