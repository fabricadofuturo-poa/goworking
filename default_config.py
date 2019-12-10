## Copiar este arquivo para instance/config.py e editar lá
## Não usar objetos, definir as variáveis tão somente
##
## Por exemplo:
## DEBUG = False
##
## ao invés de:
## class Config(object):
##   DEBUG = False

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  DEBUG = False
  TESTING = False
  SECRET_KEY = "sou um seixo rolado na estrada do lado de la do sertao"
  WTF_CSRF_SECRET_KEY = "e ser tao humilhado e sinal de que o diabo e que amassa o meu pao"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
  ## The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy that I do not need, which is to signal the application every time a change is about to be made in the database.
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
  SECRET_KEY = "mas meu corpo e discente e civilizada a mente toca cheira ouve e ve"
  WTF_CSRF_SECRET_KEY = "e com amor e anarquia goza que rosca e arrepia rock en rolando em voce"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://goworking:goworking@localhost/goworking'

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'goworking.db')

class TestingConfig(Config):
  TESTING = True
  SECRET_KEY = "no corpo rosa dos ventos tudo e norte tudo e sul"
  WTF_CSRF_SECRET_KEY = "se oriente se ocidente toda cor corre pro azul"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://gotesting:gotesting@localhost/gotesting'

