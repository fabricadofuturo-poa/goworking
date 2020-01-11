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
  NovaCadeiraForm,
  EditarCadeiraForm,
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import cadeira as cadeira_model

@bp.route('/cadeira', methods=['GET', 'POST'])
@bp.route('/cadeira/<string:cadeira_id>', methods=['GET', 'POST'])
@login_required
def cadeira(cadeira_id=None):
  cadeira_object = cadeira_model.query.filter_by(numero=u"00-A").first()
  cadeiras_object = cadeira_model.query.order_by(cadeira_model.numero).all()
  if cadeira_id is not None:
    cadeira_object = cadeira_model.query.filter_by(id=cadeira_id).first()
    if cadeira_object:
      return redirect(
        url_for(
          'goworking.cadeira_editar',
          cadeira_id=cadeira_object.id,
        )
      )
  form = NovaCadeiraForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while cadeira_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    cadeira_object = cadeira_model(
      id = id,
      numero = form.numero.data,
      ordem = form.ordem.data,
      id_mesa = form.id_mesa.data,
      desc = form.desc.data,
    )
    try:
      db.session.add(cadeira_object)
      db.session.commit()
      flash(
        u"Deu certo! Cadeira %s cadastrada"
        % (str(cadeira_object.numero)),
        'success',
      )
      return redirect(url_for('goworking.cadeira'))
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
  return render_template(
    'cadeira.html',
    title = u"Cadeiras",
    subtitle = u"Cadastrar cadeira",
    cadeira = cadeira_object,
    cadeiras = cadeiras_object,
    form = form,
  )

@bp.route('/cadeira/editar/<string:cadeira_id>', methods=['GET', 'POST'])
@login_required
def cadeira_editar(cadeira_id=None):
  cadeira_object = cadeira_model.query.filter_by(id=cadeira_id).first()
  cadeiras_object = cadeira_model.query.order_by(cadeira_model.numero).all()
  if cadeira_id is None:
    return redirect(url_for('goworking.cadeira'))
  form = EditarCadeiraForm()
  form.id.data = cadeira_object.id
  form.numero.data = cadeira_object.numero
  form.ordem.data = cadeira_object.ordem
  form.desc.data = cadeira_object.desc
  form.id_mesa.data = cadeira_object.id_mesa
  if form.validate_on_submit():
    try:
      cadeira_object.numero = form.numero.data
      cadeira_object.ordem = form.ordem.data
      cadeira_object.id_mesa = form.id_mesa.data
      cadeira_object.desc = form.desc.data
      db.session.commit()
      flash(u"Deu certo! Dados de %s atualizados" % (str(cadeira_object.numero)), 'success')
    except Exception as e:
      flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    return redirect(url_for('goworking.cadeira'))
  return render_template(
    'cadeira.html',
    title = u"Cadeiras",
    subtitle = u"Editar cadeira %s" % (cadeira_object.numero),
    cadeira = cadeira_object,
    cadeiras = cadeiras_object,
    form = form,
  )

@bp.route('/cadeira/apagar/<string:cadeira_id>', methods=['GET', 'POST'])
@login_required
def cadeira_apagar(cadeira_id=None):
  cadeira_object = cadeira_model.query.filter_by(id=cadeira_id).first()
  if cadeira_id is None:
    return redirect(url_for('goworking.cadeira'))
  cadeira_object = cadeira_model.query.filter_by(id=cadeira_id).first()
  try:
    db.session.delete(cadeira_object)
    db.session.commit()
    flash(u"Deu certo! Cadeira %s apagada" % (str(cadeira_object.numero)), 'success')
  except Exception as e:
    flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
  return redirect(url_for('goworking.cadeira'))
