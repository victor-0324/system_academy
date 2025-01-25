from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_PRIVATE_URL")
    print(SQLALCHEMY_DATABASE_URI)
class DBConnectionHandler:
    """Sqlalchemy database connection"""

    def __init__(self, db=None):
        self.db = db

    def init_app(self, app):
        self.app = app
        self.db.init_app(app)
        app.db = self.db  

    def get_connection(self):
        return self.db

    def create_all(self):
        with self.app.app_context():
            self.db.engine.connect()
            self.app.logger.info("Conexão bem-sucedida!")
            self.db.create_all()
            self.app.logger.info("Tabelas criadas com sucesso!")

    def query(self, model):
        return self.db.session.query(model)

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db.session:
            self.db.session.remove()

def db_connector(func):
    """Fornece uma conexão com o banco de dados
    connector: é uma instância de session configurada por DBConnectionHandler
    """

    def with_connection_(*args, **kwargs):
        with DBConnectionHandler(db).app.app_context():
            try:
                query = func(*args, **kwargs)
                return query
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    return with_connection_
