""" Metodo de fabrica """

from flask import Flask

def init_app():
    """Contruindo o app"""
    app = Flask(__name__)

    # Configuração do app
    app.secret_key = "vitorvitoriaeyaramariaauvesdacosta"

 

    # Database
    from .database import DBConnectionHendler
    from .database import Base

    db_connection = DBConnectionHendler()
    engine = db_connection.get_engine()
    
    with app.app_context():
       
        # Aplicativo inicial
        from .blueprints import initial_app

        app.register_blueprint(initial_app)

        # Criando tabelas que não existem e estão
        # Criando a enginer
        try:
            Base.metadata.create_all(engine)
            print("Tabelas criadas com sucesso!")
            
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")

        return app
