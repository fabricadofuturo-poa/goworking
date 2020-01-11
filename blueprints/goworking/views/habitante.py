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

import re
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
  NovaHabitanteForm,
  EditarHabitanteForm,
  custom_uuid,
)

from app import (
  db,
)

from blueprints.goworking.models import (
  habitante as habitante_model,
  cadeira as cadeira_model,
  empresa as empresa_model,
)

@bp.route('/habitante', methods=['GET', 'POST'])
@login_required
def habitante():
  try:
    habitantes_object = habitante_model.query.order_by(
      habitante_model.nome).all()
    ## Gera um uuid aleatório até que não exista nenhum idêntico no
    ## banco de dados. Mesmo que a chance hipotética de acontecer
    ## seja altamente improvável.
    id = custom_uuid.random_uuid()
    while habitante_model.query.get(id):
      id = custom_uuid.random_uuid()
    habitante_object = habitante_model(id=id)
    ## Tenta popular o formulário e o objeto habitante com os valores
    ## dos parâmetros do HTTP POST. Isto deve acontecer caso o
    ## formulário seja enviado novamente em virtude de algum erro
    ## processado pelo servidor (python) ao invés do cliente
    ## (javascript).
    if 'nome' in request.args:
      habitante_object.nome = request.args.get('nome')
    if 'cpf' in request.args:
      habitante_object.cpf = re.sub(
        r'[^\d]*',
        '',
        request.args.get('cpf'),
      )
    if 'desc' in request.args:
      habitante_object.desc = request.args.get('desc')
    if 'data_entrada' in request.args:
      habitante_object.data_entrada = datetime.strptime(
        request.args.get('data_entrada'), '%Y-%m-%d')
    if 'data_saida' in request.args:
      habitante_object.data_saida = datetime.strptime(
        request.args.get('data_saida'), '%Y-%m-%d')
    if 'data_renovacao' in request.args:
      habitante_object.data_renovacao = datetime.strptime(
        request.args.get('data_renovacao'), '%Y-%m-%d')
    form = NovaHabitanteForm(obj = habitante_object)
    if form.validate_on_submit():
      try:
        habitante_object.nome = form.nome.data
        habitante_object.cpf = re.sub(r'[^\d]*', '', form.cpf.data)
        habitante_object.desc = form.desc.data
        habitante_object.data_entrada = form.data_entrada.data
        habitante_object.data_saida = form.data_saida.data
        habitante_object.data_renovacao = form.data_renovacao.data
        if form.empresa.data is not None:
          habitante_object.id_empresa = form.empresa.data.id
      except Exception as e:
        mensagem = u"Falha tentando criar habitante! \
          Erro: %s" % (str(e))
        print(u"[DEBUG] %s" % (mensagem))
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante',
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      ## Verifica se já tem alguém nesta cadeira
      cadeira_ocupada = False
      if form.cadeira.data is not None:
        cadeira_ocupada = habitante_model.query.filter_by(
          id_cadeira = form.cadeira.data.id).first()
      if cadeira_ocupada:
        mensagem = u"Cadeira já está ocupada, escolha outra!"
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante',
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      else:
        if form.cadeira.data is not None:
          habitante_object.id_cadeira = form.cadeira.data.id
        try:
          db.session.add(habitante_object)
          db.session.commit()
          flash(
            u"Deu certo! Dados de %s cadastrados"
            % (str(habitante_object.nome)),
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
          return redirect(url_for('goworking.habitante'))
    return render_template(
      'habitante.html',
      title = u"Habitantes",
      subtitle = u"Cadastrar habitante",
      habitante = habitante_object,
      habitantes = habitantes_object,
      form = form,
    )
  except Exception as e:
    abort(500, str(e))
  abort(500)

@bp.route('/habitante/<string:id_cadeira>', methods=['GET', 'POST'])
@login_required
def habitante_cadeira(id_cadeira = custom_uuid.nil_uuid):
  try:
    habitantes_object = habitante_model.query.order_by(
      habitante_model.nome).all()
    ## Gera um uuid aleatório até que não exista nenhum idêntico no
    ## banco de dados. Mesmo que a chance hipotética de acontecer
    ## seja altamente improvável.
    id = custom_uuid.random_uuid()
    while habitante_model.query.get(id):
      id = custom_uuid.random_uuid()
    habitante_object = habitante_model(id=id, id_cadeira=id_cadeira)
    ## Tenta popular o formulário e o objeto habitante com os valores
    ## dos parâmetros do HTTP POST. Isto deve acontecer caso o
    ## formulário seja enviado novamente em virtude de algum erro
    ## processado pelo servidor (python) ao invés do cliente
    ## (javascript).
    if 'nome' in request.args:
      habitante_object.nome = request.args.get('nome')
    if 'cpf' in request.args:
      habitante_object.cpf = re.sub(
        r'[^\d]*',
        '',
        request.args.get('cpf'),
      )
    if 'desc' in request.args:
      habitante_object.desc = request.args.get('desc')
    if 'data_entrada' in request.args:
      habitante_object.data_entrada = datetime.strptime(
        request.args.get('data_entrada'), '%Y-%m-%d')
    if 'data_saida' in request.args:
      habitante_object.data_saida = datetime.strptime(
        request.args.get('data_saida'), '%Y-%m-%d')
    if 'data_renovacao' in request.args:
      habitante_object.data_renovacao = datetime.strptime(
        request.args.get('data_renovacao'), '%Y-%m-%d')
    form = NovaHabitanteForm(obj = habitante_object)
    cadeira_object = cadeira_model.query.get(id_cadeira)
    if cadeira_object:
      form.cadeira.data = cadeira_object
    if form.validate_on_submit():
      try:
        habitante_object.nome = form.nome.data
        habitante_object.cpf = re.sub(r'[^\d]*', '', form.cpf.data)
        habitante_object.desc = form.desc.data
        habitante_object.data_entrada = form.data_entrada.data
        habitante_object.data_saida = form.data_saida.data
        habitante_object.data_renovacao = form.data_renovacao.data
        if form.empresa.data is not None:
          habitante_object.id_empresa = form.empresa.data.id
      except Exception as e:
        mensagem = u"Falha tentando criar habitante! \
          Erro: %s" % (str(e))
        print(u"[DEBUG] %s" % (mensagem))
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante',
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      ## Verifica se já tem alguém nesta cadeira
      cadeira_ocupada = False
      if form.cadeira.data is not None:
        cadeira_ocupada = habitante_model.query.filter_by(
          id_cadeira = form.cadeira.data.id).first()
      if cadeira_ocupada:
        mensagem = u"Cadeira já está ocupada, escolha outra!"
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante',
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      else:
        if form.cadeira.data is not None:
          habitante_object.id_cadeira = form.cadeira.data.id
        try:
          db.session.add(habitante_object)
          db.session.commit()
          flash(
            u"Deu certo! Dados de %s cadastrados"
            % (str(habitante_object.nome)),
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
          return redirect(url_for('goworking.habitante'))
    return render_template(
      'habitante.html',
      title = u"Habitantes",
      subtitle = u"Cadastrar habitante",
      habitante = habitante_object,
      habitantes = habitantes_object,
      form = form,
    )
  except Exception as e:
    abort(500, str(e))
  abort(500)

@bp.route('/habitante/editar/<string:id>', methods=['GET', 'POST'])
@login_required
def habitante_editar(id = custom_uuid.nil_uuid):
  try:
    habitantes_object = habitante_model.query.order_by(
      habitante_model.nome).all()
    habitante_object = habitante_model.query.get(id)
    #~ form = EditarHabitanteForm()
    ## Tenta popular o formulário e o objeto habitante com os valores
    ## dos parâmetros do HTTP POST. Isto deve acontecer caso o
    ## formulário seja enviado novamente em virtude de algum erro
    ## processado pelo servidor (python) ao invés do cliente
    ## (javascript).
    if 'nome' in request.args:
      habitante_object.nome = request.args.get('nome')
    if 'cpf' in request.args:
      habitante_object.cpf = re.sub(
        r'[^\d]*',
        '',
        request.args.get('cpf'),
      )
    if 'desc' in request.args:
      habitante_object.desc = request.args.get('desc')
    if 'data_entrada' in request.args:
      habitante_object.data_entrada = datetime.strptime(
        request.args.get('data_entrada'), '%Y-%m-%d')
    if 'data_saida' in request.args:
      habitante_object.data_saida = datetime.strptime(
        request.args.get('data_saida'), '%Y-%m-%d')
    if 'data_renovacao' in request.args:
      habitante_object.data_renovacao = datetime.strptime(
        request.args.get('data_renovacao'), '%Y-%m-%d')
    form = EditarHabitanteForm(obj = habitante_object)
    #~ form.populate_obj(habitante_object)
    if form.validate_on_submit():
      try:
        if form.nome.data is not None:
          habitante_object.nome = form.nome.data
        if form.cpf.data is not None:
          habitante_object.cpf = re.sub(r'[^\d]*', '', form.cpf.data)
        if form.desc.data is not None:
          habitante_object.desc = form.desc.data
        if form.data_entrada.data is not None:
          habitante_object.data_entrada = form.data_entrada.data
        if form.data_saida.data is not None:
          habitante_object.data_saida = form.data_saida.data
        if form.data_renovacao.data is not None:
          habitante_object.data_renovacao = form.data_renovacao.data
        if form.empresa.data is not None:
          habitante_object.id_empresa = form.empresa.data.id
      except Exception as e:
        mensagem = u"Falha tentando editar habitante! \
          Erro: %s" % (str(e))
        print(u"[DEBUG] %s" % (mensagem))
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante_editar',
          id = form.id.data,
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      ## Verifica se já tem alguém nesta cadeira
      cadeira_ocupada = False
      if form.data['cadeira']:
        cadeira_ocupada = habitante_model.query.filter_by(
          id_cadeira = form.cadeira.data.id).first()
      if cadeira_ocupada and cadeira_ocupada is not habitante_object:
        mensagem = u"Cadeira já está ocupada, escolha outra!"
        flash(mensagem, 'danger')
        return redirect(url_for(
          'goworking.habitante_editar',
          id = form.id.data,
          nome = form.nome.data,
          cpf = form.cpf.data,
          desc = form.desc.data,
          data_entrada = form.data_entrada.data,
          data_saida = form.data_saida.data,
          data_renovacao = form.data_renovacao.data,
        ))
      else:
        if form.cadeira.data is not None:
          habitante_object.id_cadeira = form.cadeira.data.id
        try:
          #~ db.session.add(habitante_object)
          db.session.commit()
          flash(
            u"Deu certo! Dados de %s atualizados"
            % (str(habitante_object.nome)),
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
          return redirect(url_for('goworking.habitante'))
    return render_template(
      'habitante.html',
      title = u"Habitantes",
      subtitle = u"Editar habitante",
      habitante = habitante_object,
      habitantes = habitantes_object,
      form = form,
    )
  except Exception as e:
    abort(500, str(e))
  abort(500)

@bp.route(
  '/habitante/apagar/<string:id>',
  methods=['GET', 'POST', 'DELETE'],
)
@login_required
def habitante_apagar(id = None):
  try:
    if id is None:
      return redirect(url_for('goworking.habitante'))
    habitante_object = habitante_model.query.get(id)
    if habitante_object:
      try:
        db.session.delete(habitante_object)
        db.session.commit()
        flash(
          u"Deu certo! Dados de %s \
            apagados" % (str(habitante_object.nome)),
          'success',
        )
      except Exception as e:
        flash(u"Deu errado! O problema foi: %s" % (str(e)), 'danger')
    else:
      flash(
        u"Não tem habitante com o id %s pra apagar!" % (id),
        'warning',
      )
    return redirect(url_for('goworking.habitante'))
  except Exception as e:
    abort(500, str(e))
  abort(500)
