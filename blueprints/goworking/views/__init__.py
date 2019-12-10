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

from flask import (
  abort,
  flash,
  redirect,
  render_template,
  request,
  session,
  url_for,
)

from flask_login import (
  current_user,
  login_user,
  login_required,
  logout_user,
)

from werkzeug.urls import url_parse

import sqlalchemy
import sys

## TODO log deveria ser feito no app.py. É feito?
#import logging
#logging.basicConfig(
#  filename='instance/error.log',
#  filemode='w',
#  level=logging.ERROR,
#)

from app import db

from blueprints.goworking import bp

from blueprints.goworking.views.index import index
from blueprints.goworking.views.erros import (
  erro,
  erro_404,
  erro_500,
  erro_502,
)
from blueprints.goworking.views.login import (
  login,
  logout,
  signup,
)
from blueprints.goworking.views import (
  espaco,
  mesa,
  cadeira,
  empresa,
  habitante,
)

