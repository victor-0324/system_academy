from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from src.database.querys import Querys 

login_app = Blueprint("login_app", __name__, url_prefix="/login", template_folder='templates',static_folder='static')

@login_app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('username')
        senha = request.form.get('password')

        session = current_app.db.session
        querys_instance = Querys(session)   

        aluno, permissao = querys_instance.verificar_credenciais(login, senha) 
        print(aluno, permissao)
        if aluno:
            if permissao == 'admin':
                login_user(aluno)
                return redirect(url_for('initial_app.mostrar'))
            elif permissao == 'treino' and aluno.exercicios:
                login_user(aluno)
                return redirect(url_for('treino_app.mostrar'))
            else:
                flash('Credenciais inválidas ou acesso não autorizado. Tente novamente.', 'danger')
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    return render_template('login.html')

@login_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_app.login'))
