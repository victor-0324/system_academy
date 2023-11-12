from src.app import init_app
from src.app import load_user
from src.database.config import DBConnectionHandler, db
from src.database import Base

app, login_manager = init_app()


# Iniciar o Servidor
if __name__ == "__main__":
    
    app.run(host='0.0.0.0', debug=True, port=5000)
