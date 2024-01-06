"""Inicia a aplicação flask"""

from src import init_app

app, login_manager = init_app()

if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=5001)