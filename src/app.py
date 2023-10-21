from flask import Flask


def init_app():
    app = Flask(__name__)

    # Configuração do app
    app.secret_key = "vitorvitoriaeyaramariaauvesdacosta"

    with app.app_context(): 

         # Aplicativo inicial
        from .blueprints import initial_app

        app.register_blueprint(initial_app)

      

        return app