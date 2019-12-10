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

from blueprints.goworking import bp

from flask import render_template

from flask_login import login_required

@bp.route('/')
@login_required
def index():
  from blueprints.goworking.controllers.dummy import goworking_esqueleto
  from blueprints.goworking.models import (
    mesa as mesa_model,
    cadeira as cadeira_model,
  )
  mesas = mesa_model.query.order_by(mesa_model.ordem).all()
  cadeiras = cadeira_model.query.order_by(cadeira_model.ordem).all()
  return render_template(
    'index.html',
    espacos = goworking_esqueleto(),
    mesas = mesas,
    cadeiras = cadeiras,
    title = u"Goworking de",
  )

