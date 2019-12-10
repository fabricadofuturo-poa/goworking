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
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import mesa as mesa_model

@bp.route('/mesa', methods=['GET', 'POST'])
@bp.route('/mesa/<string:mesa_id>', methods=['GET', 'POST'])
@login_required
def mesa(mesa_id=None):
  mesa_object = mesa_model.query.filter_by(numero=u"00-A").first()
  mesas_object = mesa_model.query.all()
  if mesa_id is not None:
    mesa_object = mesa_model.query.filter_by(id=mesa_id).first()
    if mesa_object:
      return redirect(
        url_for(
          'goworking.mesa_editar',
          mesa_id=mesa_object.id,
        )
      )
  form = NovaMesaForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while mesa_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    mesa_object = mesa_model(
      id = id,
      numero = form.numero.data,
      ordem = form.ordem.data,
      desc = form.desc.data,
      id_espaco = form.id_espaco.data,
    )
    try:
      db.session.add(mesa_object)
      db.session.commit()
      flash(
        u"Deu certo! Dados de %s cadastrados"
        % (str(mesa_object.numero)),
        'success',
      )
      return redirect(url_for('goworking.mesa'))
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
  return render_template(
    'mesa.html',
    title = u"Mesas",
    subtitle = u"Cadastrar mesa",
    mesa = mesa_object,
    mesas = mesas_object,
    form = form,
  )

@bp.route('/mesa/editar/<string:mesa_id>', methods=['GET', 'POST'])
@login_required
def mesa_editar(mesa_id=None):
  mesa_object = mesa_model.query.filter_by(id=mesa_id).first()
  mesas_object = mesa_model.query.all()
  if mesa_id is None:
    return redirect(url_for('goworking.mesa'))
  form = EditarMesaForm()
  form.id.data = mesa_object.id
  form.numero.data = mesa_object.numero
  form.ordem.data = mesa_object.ordem
  form.desc.data = mesa_object.desc
  form.id_espaco.data = mesa_object.id_espaco
  if form.validate_on_submit():
    try:
      mesa_object.numero = form.numero.data
      mesa_object.ordem = form.ordem.data
      mesa_object.desc = form.desc.data
      mesa_object.id_espaco = form.id_espaco.data
      db.session.commit()
      flash(u"Deu certo! Dados de %s atualizados" % (str(mesa_object.numero)), 'success')
    except Exception as e:
      flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    return redirect(url_for('goworking.mesa'))
  return render_template(
    'mesa.html',
    title = u"Mesas",
    subtitle = u"Editar %s" % (mesa_object.nome),
    mesa = mesa_object,
    mesas = mesas_object,
    form = form,
  )

@bp.route('/mesa/apagar/<string:mesa_id>', methods=['GET', 'POST'])
@login_required
def mesa_apagar(mesa_id=None):
  mesa_object = mesa_model.query.filter_by(id=mesa_id).first()
  mesas_object = mesa_model.query.all()
  if mesa_id is None:
    return redirect(url_for('goworking.mesa'))
  mesa_object = mesa_model.query.filter_by(id=mesa_id).first()
  try:
    db.session.delete(mesa_object)
    db.session.commit()
    flash(u"Deu certo! Dados de %s apagados" % (str(mesa_object.numero)), 'success')
  except Exception as e:
    flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
  return redirect(url_for('goworking.mesa'))

