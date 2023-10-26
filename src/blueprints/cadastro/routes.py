from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import  Querys

cadastro_app = Blueprint("cadastro_app", __name__, url_prefix="/cadastro", template_folder='templates',static_folder='static')

# Tela Iniciarl do app
@cadastro_app.route("/", methods=["GET", "POST"])
def cadastrar():
    if request.method == 'POST':
      nome = request.form['nome']
      idade = request.form['idade']
      sexo = request.form['sexo']
      altura = request.form['altura']
      peso = request.form['peso']
      email = request.form['email']
      telefone = request.form['telefone']
      login = request.form['login']
      senha = request.form['senha']
      dia_semana = request.form['dia_semana']
      tipo_treino = request.form['tipo-treino']
      horario = request.form['horario']
      inicio = request.form['inicio']
      obj = request.form['obj']
      Querys.cadastrar_aluno(nome, idade, sexo, altura, peso, email, telefone, login, senha, dia_semana, tipo_treino, horario, inicio, obj)
      return redirect(url_for("clientes_app.mostrar"))
    
    return render_template("cadastro.html") 


  