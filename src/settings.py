# pylint: disable=too-few-public-methods
"""Configurações para o projeto
Para passar determinadas variaveis e constantes para o sistemas
esteremos utilizando objetos com diferentes propriedades para
cada ambiente. Para setar esse ambiente va para
"""

import getpass
import os
from os.path import join

from dotenv import load_dotenv


class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    MYSQL_PRIVATE_URL = os.getenv("MYSQL_PRIVATE_URL")

class DevelopmentConfig(Config):

    DEBUG = True

