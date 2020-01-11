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
  NovaEspacoForm,
  EditarEspacoForm,
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import espaco as espaco_model

@bp.route('/espaco', methods=['GET', 'POST'])
@bp.route('/espaco/<string:espaco_id>', methods=['GET', 'POST'])
@login_required
def espaco(espaco_id=None):
  espaco_object = espaco_model.query.filter_by(numero=u"00").first()
  espacos_object = espaco_model.query.order_by(espaco_model.numero).all()
  if espaco_id is not None:
    espaco_object = espaco_model.query.filter_by(id=espaco_id).first()
    if espaco_object:
      return redirect(
        url_for(
          'goworking.espaco_editar',
          espaco_id=espaco_object.id,
        )
      )
  form = NovaEspacoForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while espaco_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    espaco_object = espaco_model(
      id = id,
      numero = form.numero.data,
      ordem = form.ordem.data,
      desc = form.desc.data,
    )
    try:
      db.session.add(espaco_object)
      db.session.commit()
      flash(
        u"Deu certo! Espaço %s cadastrado"
        % (str(espaco_object.numero)),
        'success',
      )
      return redirect(url_for('goworking.espaco'))
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
      return redirect(url_for('goworking.espaco'))
  return render_template(
    'espaco.html',
    title = u"Espaços",
    subtitle = u"Cadastrar espaço",
    espaco = espaco_object,
    espacos = espacos_object,
    form = form,
  )

@bp.route('/espaco/editar/<string:espaco_id>', methods=['GET', 'POST'])
@login_required
def espaco_editar(espaco_id=None):
  espaco_object = espaco_model.query.filter_by(id=espaco_id).first()
  espacos_object = espaco_model.query.order_by(espaco_model.numero).all()
  if espaco_id is None:
    return redirect(url_for('goworking.espaco'))
  form = EditarEspacoForm()
  form.id.data = espaco_object.id
  form.numero.data = espaco_object.numero
  form.ordem.data = espaco_object.ordem
  form.desc.data = espaco_object.desc
  if form.validate_on_submit():
    try:
      espaco_object.numero = form.numero.data
      espaco_object.ordem = form.ordem.data
      espaco_object.desc = form.desc.data
      db.session.commit()
      flash(u"Deu certo! Espaço %s atualizado" % (str(espaco_object.numero)), 'success')
    except Exception as e:
      flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    return redirect(url_for('goworking.espaco'))
  return render_template(
    'espaco.html',
    title = u"Espaços",
    subtitle = u"Editar espaço %s" % (espaco_object.numero),
    espaco = espaco_object,
    espacos = espacos_object,
    form = form,
  )

@bp.route('/espaco/apagar/<string:espaco_id>', methods=['GET', 'POST'])
@login_required
def espaco_apagar(espaco_id=None):
  espaco_object = espaco_model.query.filter_by(id=espaco_id).first()
  if espaco_id is None:
    return redirect(url_for('goworking.espaco'))
  espaco_object = espaco_model.query.filter_by(id=espaco_id).first()
  try:
    db.session.delete(espaco_object)
    db.session.commit()
    flash(u"Deu certo! Espaço %s apagado" % (str(espaco_object.numero)), 'success')
  except Exception as e:
    flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
  return redirect(url_for('goworking.espaco'))
