""" Configs from database conncetions"""
# pylint: disable=unused-argument, no-member, arguments-differ, no-value-for-parameter, unreachable, pylint(import-error),pylint(unused-import)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




class DBConnectionHendler:
    """Sqlalchemy database connection"""

    def __init__(self) -> None:
        self.__connection_string = "mariadb+mariadbconnector://bingogn:bingo_game@127.0.0.1:3306/enovare"
        self.session = None

    def get_engine(self):
        """Return connection engine
        :param - None
        :return - engine_connection
        """
        engine = create_engine(self.__connection_string)
        return engine

    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()  


def db_connector(func):
    """Fornece uma conexão com o banco de dados
    connector: é um instancia de session configuradapor DBConnectionHendler
    """

    def with_connection_(cls, *args):
        with DBConnectionHendler() as connection:
            try:
                query = func(cls, connection, *args)
                return query
            except:
                connection.session.rollback()
                raise
            finally:
                connection.session.close()

    return with_connection_
