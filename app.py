# vim:fileencoding=utf-8
#  Go Working - Controle das Mesas
#  
#  Copyright (C) 2019-2020 Fábrica do Futuro
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  

## Flask
from flask import (
  Flask,
  redirect,
  url_for,
)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('default_config.Config')
try:
  app.config.from_pyfile(''.join([app.instance_path, '/config.py']))
except Exception as e:
  print(u"Arquivo de configuração não encontrado. Exceção: %s" % (e))

## Flask WTF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

## Flask Login
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'goworking.login'
login_manager.login_message = u"Por favor identifique-se"
login_manager.login_message_category = 'info'

## Flask SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type = True)

## Log
## TODO não sei se funciona desta forma os logs, provavelmente somente uma destas configurações (a última?) esteja funcionando de fato.
import logging
logging.basicConfig(filename='instance/error.log', filemode='w', level=logging.ERROR)
logging.basicConfig(filename='instance/info.log', filemode='w', level=logging.INFO)
logging.basicConfig(filename='instance/debug.log', filemode='w', level=logging.DEBUG)

## Index
@app.route("/")
def index():
  return redirect(url_for('goworking.index'))

## Blueprints
## API
## TODO APi deve ser utilizada programaticamente como API propriamente dita,
## aida há trabalho a ser feito para se tornar uma API de fato.
#from blueprints.api import bp as api_bp
#app.register_blueprint(api_bp, url_prefix="/api")
## Web
## TODO blueprint criado para centralizar os arquivos de /static
#from blueprints.web import bp as web_bp
#app.register_blueprint(web_bp, url_prefix="/web")
## Go Working
from blueprints.goworking import bp as goworking_bp
app.register_blueprint(goworking_bp, url_prefix="/goworking")

## Flask shell
@app.shell_context_processor
def make_shell_context():
  from blueprints.goworking.controllers.dummy import dados_mesas
  from copy import deepcopy
  return {'db': db, 'map': app.url_map, 'dados': deepcopy(dados_mesas())}

# ~ login.init_app(app)
# ~ db.init_app(app)
# ~ migrate.init_app(app)
# ~ print(app.url_map)

