"""Inicia a aplicação flask"""

from src.app import init_app
from src.database.config import DevelopmentConfig


app, login_manager = init_app()

app.config.from_object(DevelopmentConfig)


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=5000)