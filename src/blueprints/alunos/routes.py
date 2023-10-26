from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import Querys

clientes_app = Blueprint("clientes_app", __name__, url_prefix="/alunos", template_folder='templates',static_folder='static')

# Tela Iniciarl do app
@clientes_app.route("/", methods=["GET", "POST"])
def mostrar():
    alunos = Querys.mostrar()
    quantidade_alunos = len(alunos)
    return render_template("alunos.html",alunos=alunos, quantidade_alunos=quantidade_alunos)


@clientes_app.route("/detalhes/<int:aluno_id>", methods=["GET"])
def mostrar_detalhes(aluno_id):
    aluno = Querys.mostrar_detalhes(aluno_id) 
   
    return render_template('detalhes.html', aluno=aluno)



@clientes_app.route("/deletar/<int:aluno_id>", methods=["GET", "POST"])
def deletar(aluno_id):
    Querys.deletar(aluno_id)
    return redirect(url_for("clientes_app.mostrar"))

@clientes_app.route('/pesquisar_alunos', methods=['POST'])
def pesquisar_alunos():
    termo_pesquisa = request.form.get('termo_pesquisa', '').lower()
    
    # Lógica de pesquisa no backend (substitua pela sua lógica real)
    resultados = [aluno for aluno in alunos if termo_pesquisa in aluno['nome'].lower()]

    return jsonify(resultados)