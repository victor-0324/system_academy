from src.database.config import DBConnectionHendler, db_connector
from src.database.models import Admin

class AdminsQuerys:
    """Querys para manipulação de admins"""

    @classmethod
    @db_connector
    def add_admin(cls, connection, nome, login, senha):
        """Adiciona um novo admin ao banco de dados"""
        admin = Admin(nome=nome, login=login, senha=senha)

        connection.session.add(admin)
        connection.session.commit()

    @classmethod
    @db_connector
    def mostrar_admins(cls, connection):
        """Retorna uma lista de todos os admins"""
        admins = connection.session.query(Admin)
        return admins
