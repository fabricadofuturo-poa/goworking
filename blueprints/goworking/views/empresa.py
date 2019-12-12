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
  NovaEmpresaForm,
  EditarEmpresaForm,
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import empresa as empresa_model

@bp.route('/empresa', methods=['GET', 'POST'])
@bp.route('/empresa/<string:empresa_id>', methods=['GET', 'POST'])
@login_required
def empresa(empresa_id=None):
  empresa_object = empresa_model.query.filter_by(nome=u"Nenhuma").first()
  empresas_object = empresa_model.query.order_by(empresa_model.nome).all()
  if empresa_id is not None:
    empresa_object = empresa_model.query.filter_by(id=empresa_id).first()
    if empresa_object:
      return redirect(
        url_for(
          'goworking.empresa_editar',
          empresa_id=empresa_object.id,
        )
      )
  form = NovaEmpresaForm()
  if form.validate_on_submit():
    ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
    ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
    id = custom_uuid.random_uuid()
    while empresa_model.query.filter_by(id=id).first():
      id = custom_uuid.random_uuid()
    empresa_object = empresa_model(
      id=id,
      nome=form.nome.data,
      cnpj=form.cnpj.data,
      desc=form.desc.data,
    )
    try:
      db.session.add(empresa_object)
      db.session.commit()
      flash(
        u"Deu certo! Empresa %s cadastrada"
        % (str(empresa_object.nome)),
        'success',
      )
      return redirect(url_for('goworking.empresa'))
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
      return redirect(url_for('goworking.empresa'))
  return render_template(
    'empresa.html',
    title = u"Empresas",
    subtitle = u"Cadastrar empresa",
    empresa = empresa_object,
    empresas = empresas_object,
    form = form,
  )

@bp.route('/empresa/editar/<string:empresa_id>', methods=['GET', 'POST'])
@login_required
def empresa_editar(empresa_id=None):
  empresa_object = empresa_model.query.filter_by(id=empresa_id).first()
  empresas_object = empresa_model.query.order_by(empresa_model.nome).all()
  if empresa_id is None:
    return redirect(url_for('goworking.empresa'))
  form = EditarEmpresaForm()
  form.id.data = empresa_object.id
  form.nome.data = empresa_object.nome
  form.cnpj.data = empresa_object.cnpj
  form.desc.data = empresa_object.desc
  if form.validate_on_submit():
    try:
      empresa_object.nome = form.nome.data
      empresa_object.cnpj = form.cnpj.data
      empresa_object.desc = form.desc.data
      db.session.commit()
      flash(u"Deu certo! Dados de %s atualizados" % (str(empresa_object.nome)), 'success')
    except Exception as e:
      flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    return redirect(url_for('goworking.empresa'))
  return render_template(
    'empresa.html',
    title = u"Empresas",
    subtitle = u"Editar empresa %s" % (empresa_object.nome),
    empresa = empresa_object,
    empresas = empresas_object,
    form = form,
  )

@bp.route('/empresa/apagar/<string:empresa_id>', methods=['GET', 'POST'])
@login_required
def empresa_apagar(empresa_id=None):
  empresa_object = empresa_model.query.filter_by(id=empresa_id).first()
  if empresa_id is None:
    return redirect(url_for('goworking.empresa'))
  empresa_object = empresa_model.query.filter_by(id=empresa_id).first()
  try:
    db.session.delete(empresa_object)
    db.session.commit()
    flash(u"Deu certo! Dados da empresa %s apagados" % (str(empresa_object.nome)), 'success')
  except Exception as e:
    flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
  return redirect(url_for('goworking.empresa'))
