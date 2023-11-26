from flask import Flask
from src.app import init_app
from src.app import load_user
from src.database.config import DBConnectionHandler, db
from src.database import Base
from src.database.config import DevelopmentConfig

# Inicializar a aplicação
app, login_manager = init_app()

# Carregar as configurações
app.config.from_object(DevelopmentConfig)


# Iniciar o Servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)