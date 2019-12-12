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

from blueprints.goworking.models import (
  espaco as espaco_model,
  mesa as mesa_model,
  cadeira as cadeira_model,
  habitante as habitante_model,
  empresa as empresa_model,
)

@bp.route('/')
@login_required
def index():
  espacos = espaco_model.query.order_by(espaco_model.ordem).all()
  mesas = mesa_model.query.order_by(mesa_model.ordem).all()
  cadeiras = cadeira_model.query.order_by(cadeira_model.ordem).all()
  habitantes = habitante_model.query.order_by(habitante_model.nome).all()
  empresas = empresa_model.query.order_by(empresa_model.nome).all()
  return render_template(
    'index.html',
    espacos = espacos,
    mesas = mesas,
    cadeiras = cadeiras,
    habitantes = habitantes,
    empresas = empresas,
    title = u"GoWorking",
  )

@bp.route('/admin')
@login_required
def admin():
  from blueprints.goworking.controllers.db.dummy import goworking_esqueleto
  mesas = mesa_model.query.order_by(mesa_model.ordem).all()
  cadeiras = cadeira_model.query.order_by(cadeira_model.ordem).all()
  from blueprints.goworking.controllers.db import populate
  populate.popular_espacos()
  populate.popular_mesas()
  return render_template(
    'admin.html',
    espacos = goworking_esqueleto(),
    mesas = mesas,
    cadeiras = cadeiras,
    title = u"Goworking de",
  )
