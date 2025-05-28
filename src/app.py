from flask import Flask, current_app
from flask_login import LoginManager
from src.database.config import db, DBConnectionHandler, DevelopmentConfig
from src.database import Base
from src.database.models import Aluno

login_manager = LoginManager()

def load_user(user_id):
    with DBConnectionHandler(current_app.db) as connection:
        connection = DBConnectionHandler(db)
        user = connection.query(Aluno).get(int(user_id))
        print(user)
        return user

def init_app():
    """Construindo o app"""
    app = Flask(__name__)
    app.config.from_object("src.database.config.DevelopmentConfig")
   
    login_manager.init_app(app)
    login_manager.login_view = 'login_app.login'
    login_manager.user_loader(load_user)
  
    # Importar blueprints após a criação do aplicativo
    from .blueprints import login_app, initial_app, cadastro_app, clientes_app, treino_app

    # Registrar blueprints
    app.register_blueprint(login_app)
    app.register_blueprint(initial_app)
    app.register_blueprint(cadastro_app)
    app.register_blueprint(clientes_app)
    app.register_blueprint(treino_app)
    db_handler = DBConnectionHandler(db)
    db_handler.init_app(app)
    
    with app.app_context():
        Base.metadata.create_all(db_handler.get_connection().engine)
    
    return app, login_manager
