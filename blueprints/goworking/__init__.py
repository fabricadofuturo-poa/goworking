# vim:fileencoding=utf-8
#  Go Working - Controle das Mesas
#  
#  Copyright (C) 2019 Fábrica do Futuro
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

from app import (
  app,
  login_manager,
)
from flask import (
  flash,
  redirect,
  url_for,
)
from blueprints.goworking.models import User

## Jinja
from blueprints.goworking.controllers.filters import (
  filtro_data,
  filtro_tjemse,
)
app.jinja_env.filters['data'] = filtro_data
app.jinja_env.filters['nome'] = filtro_tjemse

## Blueprint
from flask import Blueprint
bp = Blueprint('goworking', __name__, static_folder='static', template_folder='templates', url_prefix='/goworking', root_path='blueprints/goworking')

@login_manager.unauthorized_handler
def unauthorized():
  flash(
    u"Faça login para ver esta página.",
    'warning',
  )
  return redirect(url_for('goworking.login'))

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)

## GoWorking
from blueprints.goworking import views, models, controllers

