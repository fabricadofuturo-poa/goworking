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

from flask import (
  flash,
  redirect,
  request,
  render_template,
  url_for,
)

from flask_login import login_required

from blueprints.goworking.controllers import (
  NovaMesaForm,
  EditarMesaForm,
  NovaCadeiraForm,
  EditarCadeiraForm,
  NovaEmpresaForm,
  EditarEmpresaForm,
  NovaHabitanteForm,
  EditarHabitanteForm,
  custom_uuid,
)

from app import (
  db,
  login_manager,
  logging,
)

from blueprints.goworking.models import habitante as habitante_model

from blueprints.goworking.views.habitante import habitante
from blueprints.goworking.views.empresa import empresa

@bp.route('/mesa', methods=['GET', 'POST'])
@bp.route('/mesa/<string:mesa_id>', methods=['GET', 'POST'])
@login_required
def mesa(mesa_id=None):
  from blueprints.goworking.models import mesa as mesa_model
  mesas_object = mesa_model.query.all()
  if mesa_id is not None:
    mesa_object = mesa_model.query.filter_by(id=mesa_id).first()
    if mesa_object:
      form = EditarMesaForm()
      form.populate_obj(mesa_object)
      if form.validate_on_submit():
        try:
          db.update(mesa_object)
          db.session.commit()
          flash(u"Deu certo! Dados inseridos: %s" % (str(mesa_object)), 'success')
        except Exception as e:
          flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
      return redirect(url_for('goworking.mesa', mesa_id=mesa_object.id))
  form = NovaMesaForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while mesa_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    mesa_object = mesa_model(id=id, numero=form.numero.data, ordem=int(form.ordem.data))
    try:
      db.session.add(mesa_object)
      db.session.commit()
      flash(u"Deu certo! Dados inseridos: %s" % (str(mesa_object)), 'success')
      return redirect(url_for('goworking.mesa', mesa_id=mesa_object.id))
    except Exception as e:
#      logging.exception(e)
      ## TODO DEBUG
      print(u"[DEBUG]: %s" % (str(e)))
      db.session.rollback()
      db.session.remove()
      flash(
        u"Não deu certo! O problema foi o seguinte: %s"
        % (str(e)),
        'danger',
      )
      return redirect(url_for('goworking.mesa'))
  return render_template('mesa.html', title=u"Mesa", mesas=mesas_object, form=form)

@bp.route('/cadeira', methods=['GET', 'POST'])
@bp.route('/cadeira/<string:cadeira_id>', methods=['GET', 'POST'])
@login_required
def cadeira(cadeira_id=None):
  from blueprints.goworking.models import cadeira as cadeira_model
  cadeiras_object = cadeira_model.query.all()
  if cadeira_id is not None:
    cadeira_object = cadeira_model.query.filter_by(id=cadeira_id).first()
    if cadeira_object:
      form = EditarCadeiraForm()
      form.populate_obj(cadeira_object)
      if form.validate_on_submit():
        try:
          db.update(cadeira_object)
          db.session.commit()
          flash(u"Deu certo! Dados inseridos: %s" % (str(cadeira_object)), 'success')
        except Exception as e:
          flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
      return redirect(url_for('goworking.cadeira', cadeira_id=cadeira_object.id))
  form = NovaCadeiraForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while cadeira_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    cadeira_object = cadeira_model(id=id, numero=form.numero.data, ordem=form.ordem.data, id_mesa=form.id_mesa.data)
    try:
      db.session.add(cadeira_object)
      db.session.commit()
      flash(u"Deu certo! Dados inseridos: %s" % (str(cadeira_object)), 'success')
      return redirect(url_for('goworking.cadeira', cadeira_id=cadeira_object.id))
    except Exception as e:
#      logging.exception(e)
      ## TODO DEBUG
      print(u"[DEBUG]: %s" % (str(e)))
      db.session.rollback()
      db.session.remove()
      flash(
        u"Não deu certo! O problema foi o seguinte: %s"
        % (str(e)),
        'danger',
      )
      return redirect(url_for('goworking.cadeira'))
  return render_template('cadeira.html', title=u"Cadeira", cadeiras=cadeiras_object, form=form)

