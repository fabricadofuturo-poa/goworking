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

from datetime import datetime

from blueprints.goworking import bp

from flask import (
  abort,
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
@login_required
def empresa():
  try:
    empresas_object = empresa_model.query.order_by(
      empresa_model.nome).all()
    ## Gera um uuid aleatório até que não exista nenhum idêntico no
    ## banco de dados. Mesmo que a chance hipotética de acontecer
    ## seja altamente improvável.
    id = custom_uuid.random_uuid()
    while empresa_model.query.get(id):
      id = custom_uuid.random_uuid()
    empresa_object = empresa_model(id=id)
    ## Tenta popular o formulário e o objeto empresa com os valores
    ## dos parâmetros do HTTP POST. Isto deve acontecer caso o
    ## formulário seja enviado novamente em virtude de algum erro
    ## processado pelo servidor (python) ao invés do cliente
    ## (javascript).
    if 'nome' in request.args:
      empresa_object.nome = request.args.get('nome')
    if 'cnpj' in request.args:
      empresa_object.cnpj = request.args.get('cnpj')
    if 'desc' in request.args:
      empresa_object.desc = request.args.get('desc')
    form = NovaEmpresaForm(obj = empresa_object)
    if form.validate_on_submit():
      try:
        empresa_object.nome = form.nome.data
        empresa_object.cnpj = form.cnpj.data
        empresa_object.desc = form.desc.data
        if form.empresa.data is not None:
          empresa_object.id_empresa = form.empresa.data.id
      except Exception as e:
        mensagem = u"Falha tentando criar empresa! \
          Erro: %s" % (str(e))
        print(u"[DEBUG] %s" % (mensagem))
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.empresa',
          nome = form.nome.data,
          cnpj = form.cnpj.data,
        ))
      try:
        db.session.add(empresa_object)
        db.session.commit()
        flash(
          u"Deu certo! Dados de %s cadastrados"
          % (str(empresa_object.nome)),
          'success',
        )
      except Exception as e:
        db.session.rollback()
        db.session.remove()
        #~ logging.exception(e)
        mensagem = u"Não deu certo! O problema foi o seguinte: \
          %s" % (str(e))
        print(u"[DEBUG]: %s" % (mensagem))
        flash(mensagem, 'danger')
      finally:
        return redirect(url_for('goworking.empresa'))
    return render_template(
      'empresa.html',
      title = u"Empresas",
      subtitle = u"Cadastrar empresa",
      empresa = empresa_object,
      empresas = empresas_object,
      form = form,
    )
  except Exception as e:
    abort(500, str(e))
  abort(500)

@bp.route('/empresa/editar/<string:id>', methods=['GET', 'POST'])
@login_required
def empresa_editar(id = custom_uuid.nil_uuid):
  try:
    empresas_object = empresa_model.query.order_by(
      empresa_model.nome).all()
    empresa_object = empresa_model.query.get(id)
    #~ form = EditarEmpresaForm()
    ## Tenta popular o formulário e o objeto empresa com os valores
    ## dos parâmetros do HTTP POST. Isto deve acontecer caso o
    ## formulário seja enviado novamente em virtude de algum erro
    ## processado pelo servidor (python) ao invés do cliente
    ## (javascript).
    if 'nome' in request.args:
      empresa_object.nome = request.args.get('nome')
    if 'cnpj' in request.args:
      empresa_object.cnpj = request.args.get('cnpj')
    if 'desc' in request.args:
      empresa_object.desc = request.args.get('desc')
    form = EditarEmpresaForm(obj = empresa_object)
    #~ form.populate_obj(empresa_object)
    if form.validate_on_submit():
      try:
        if form.nome.data is not None:
          empresa_object.nome = form.nome.data
        if form.cnpj.data is not None:
          empresa_object.cnpj = form.cnpj.data
        if form.desc.data is not None:
          empresa_object.desc = form.desc.data
      except Exception as e:
        mensagem = u"Falha tentando editar empresa! \
          Erro: %s" % (str(e))
        print(u"[DEBUG] %s" % (mensagem))
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.empresa_editar',
          id = form.id.data,
          nome = form.nome.data,
          cnpj = form.cnpj.data,
          desc = form.desc.data,
        ))
      try:
        #~ db.session.add(empresa_object)
        db.session.commit()
        flash(
          u"Deu certo! Dados de %s atualizados"
          % (str(empresa_object.nome)),
          'success',
        )
      except Exception as e:
        db.session.rollback()
        db.session.remove()
        #~ logging.exception(e)
        mensagem = u"Não deu certo! O problema foi o seguinte: \
          %s" % (str(e))
        print(u"[DEBUG]: %s" % (mensagem))
        flash(mensagem, 'danger')
      finally:
        return redirect(url_for('goworking.empresa'))
    return render_template(
      'empresa.html',
      title = u"Empresas",
      subtitle = u"Editar empresa",
      empresa = empresa_object,
      empresas = empresas_object,
      form = form,
    )
  except Exception as e:
    abort(500, str(e))
  abort(500)

@bp.route(
  '/empresa/apagar/<string:id>',
  methods=['GET', 'POST', 'DELETE'],
)
@login_required
def empresa_apagar(id = None):
  try:
    if id is None:
      return redirect(url_for('goworking.empresa'))
    empresa_object = empresa_model.query.get(id)
    if empresa_object:
      try:
        db.session.delete(empresa_object)
        db.session.commit()
        flash(
          u"Deu certo! Dados de %s \
            apagados" % (str(empresa_object.nome)),
          'success',
        )
      except Exception as e:
        flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    else:
      flash(
        u"Não tem empresa com o id %s pra apagar!" % (id),
        'warning',
      )
    return redirect(url_for('goworking.empresa'))
  except Exception as e:
    abort(500, str(e))
  abort(500)
