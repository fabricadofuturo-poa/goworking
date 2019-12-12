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
  NovaHabitanteForm,
  EditarHabitanteForm,
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import habitante as habitante_model

@bp.route('/habitante', methods=['GET', 'POST'])
@bp.route('/habitante/<string:habitante_id>', methods=['GET', 'POST'])
@login_required
def habitante(habitante_id=None):
  habitante_object = habitante_model.query.filter_by(nome=u"Ninguém").first()
  habitantes_object = habitante_model.query.order_by(habitante_model.nome).all()
  if habitante_id is not None:
    habitante_object = habitante_model.query.filter_by(id=habitante_id).first()
    if habitante_object:
      return redirect(
        url_for(
          'goworking.habitante_editar',
          habitante_id=habitante_object.id,
        )
      )
  form = NovaHabitanteForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while habitante_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    habitante_object = habitante_model(
      id=id,
      nome=form.nome.data,
      cpf=form.cpf.data,
      desc=form.desc.data,
    )
    try:
      habitante_object.id_empresa = form.id_empresa.data.id
    except Exception as e:
      print(u"[DEBUG]: %s" % (e))
    try:
      habitante_object.id_cadeira = form.id_cadeira.data.id
    except Exception as e:
      print(u"[DEBUG]: %s" % (e))
    try:
      db.session.add(habitante_object)
      db.session.commit()
      flash(
        u"Deu certo! Dados de %s cadastrados"
        % (str(habitante_object.nome)),
        'success',
      )
      return redirect(url_for('goworking.habitante'))
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
      return redirect(url_for('goworking.habitante'))
  return render_template(
    'habitante.html',
    title = u"Habitantes",
    subtitle = u"Cadastrar habitante",
    habitante = habitante_object,
    habitantes = habitantes_object,
    form = form,
  )

@bp.route('/habitante/editar/<string:habitante_id>', methods=['GET', 'POST'])
@login_required
def habitante_editar(habitante_id=None):
  habitante_object = habitante_model.query.filter_by(id=habitante_id).first()
  habitantes_object = habitante_model.query.order_by(habitante_model.nome).all()
  if habitante_id is None:
    return redirect(url_for('goworking.habitante'))
  form = EditarHabitanteForm()
  form.id.data = habitante_object.id
  form.nome.data = habitante_object.nome
  form.cpf.data = habitante_object.cpf
  form.desc.data = habitante_object.desc
  try:
    form.id_empresa.data = habitante_object.empresa
  except Exception as e:
    print(u"[DEBUG]: %s" % (e))
  try:
    form.id_cadeira.data = habitante_object.cadeira
  except Exception as e:
    print(u"[DEBUG]: %s" % (e))
  #~ form.populate_obj(habitante_object)
  if form.validate_on_submit():
    print(habitante_object.id_empresa)
    try:
      habitante_object.nome = form.nome.data
      habitante_object.cpf = form.cpf.data
      habitante_object.desc = form.desc.data
      print(habitante_object.id_empresa)
      try:
        habitante_object.id_empresa = form.id_empresa.data.id
        print(habitante_object.id_empresa)
      except Exception as e:
        print(u"[DEBUG]: %s" % (e))
      try:
        habitante_object.id_cadeira = form.id_cadeira.data.id
      except Exception as e:
        print(u"[DEBUG]: %s" % (e))
      try:
        db.session.merge(habitante_object)
      except Exception as e:
        print(u"[DEBUG]: %s" % (e))
        db.session.rollback()
      print(habitante_object.id_empresa)
      db.session.commit()
      flash(u"Deu certo! Dados de %s atualizados" % (str(habitante_object.nome)), 'success')
    except Exception as e:
      flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    return redirect(url_for('goworking.habitante'))
  return render_template(
    'habitante.html',
    title = u"Habitantes",
    subtitle = u"Editar habitante %s" % (habitante_object.nome),
    habitante = habitante_object,
    habitantes = habitantes_object,
    form = form,
  )

@bp.route('/habitante/apagar/<string:habitante_id>', methods=['GET', 'POST'])
@login_required
def habitante_apagar(habitante_id=None):
  habitante_object = habitante_model.query.filter_by(id=habitante_id).first()
  if habitante_id is None:
    return redirect(url_for('goworking.habitante'))
  habitante_object = habitante_model.query.filter_by(id=habitante_id).first()
  try:
    db.session.delete(habitante_object)
    db.session.commit()
    flash(u"Deu certo! Dados de %s apagados" % (str(habitante_object.nome)), 'success')
  except Exception as e:
    flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
  return redirect(url_for('goworking.habitante'))
