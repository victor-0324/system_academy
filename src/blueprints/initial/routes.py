from flask import Blueprint, request, render_template, url_for, redirect
from src.database.querys import Querys
from functools import wraps
from flask_login import current_user

initial_app = Blueprint("initial_app", __name__, url_prefix="/", template_folder='templates',static_folder='static')

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
@initial_app.route("/", methods=["GET", "POST"])
@admin_required
def mostrar():
    return render_template("index.html")
    