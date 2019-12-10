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

from flask import (
  abort,
  flash,
  redirect,
  render_template,
  request,
  session,
  url_for,
)

from flask_login import (
  current_user,
  login_user,
  login_required,
  logout_user,
)

from werkzeug.urls import url_parse

import sqlalchemy
import sys

## TODO log deveria ser feito no app.py. É feito?
#import logging
#logging.basicConfig(filename='instance/error.log', filemode='w', level=logging.ERROR)

from app import db

from blueprints.goworking import bp

from blueprints.goworking.views.index import index
from blueprints.goworking.views.erros import erro, erro_404, erro_500, erro_502
from blueprints.goworking.views.login import login, logout, signup
from blueprints.goworking.views.goworking import (
  mesa,
  cadeira,
  empresa,
  habitante,
)










## Great Flask MVP
#from blueprints.goworking.views.webadmin import web_igee, web_origem, web_filosofia, web_achologia, web_igee_filosofia, web_igee_achologia
#from blueprints.goworking.views.api import db_origem, db_origem_v3, db_origem_add, db_tema, db_tema_add, db_formato, db_formato_add, db_igee, db_igee_v3, db_greatalk, db_alimento

#from blueprints.api import bp

#from flask import render_template, redirect, url_for, flash, request, session, abort
#from flask import render_template
#from flask_login import current_user, login_user, logout_user, login_required
#from flask_login import login_required







#@bp.route('/feedback', methods=['GET', 'POST'])
#@bp.route('/alimento', methods=['GET', 'POST'])
#@login_required
#def alimento():
#  from blueprints.igee.models import alimento_v3 as alimento_model
#  form = AlimentoForm()
#  if form.validate_on_submit():
#    alimento_object = alimento_model(uuid_igee=current_user.id,feedback=form.feedback.data)
#    db.session.add(alimento_object)
#    db.session.commit()
#    return redirect(url_for('obrigado'))
#  return render_template('alimento.html', title=u"Me alimente, nos alimente!", form=form)

### Web Admin

##from blueprints.api import bp
##from app import db
##from flask_login import login_required
##from blueprints.api.controllers.forms import NovoIgeeForm, NovaOrigemForm, NovaFilosofiaForm, AssociarOrigemForm, AssociarFilosofiaForm

#@bp.route('/web_igee', methods=['GET', 'POST'])
##@login_required
#def web_igee():
#  from blueprints.igee.models import igee as igee_model
#  igees = igee_model.query.all()
#  form = NovoIgeeForm()
#  if form.validate_on_submit():
#    igee_object = igee_model(igee=form.igee.data, nome=form.nome.data)
#    igee_object.igee = form.igee.data
#    igee_object.nome = form.nome.data
#    try:
#      db.session.add(igee_object)
#      db.session.commit()
#      flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(igee_object)), 'success')
#    except Exception as e:
#      db.session.rollback()
#      db.session.remove()
#      flash(u"Deu adubo! O problema foi o seguinte: %s" % (str(e)), 'danger')
#    return redirect(url_for('web_igee'))
#  return render_template('igee.html', title=u"Busca de iGees no banco", form=form, dados=igees)

#@bp.route('/web_origem', methods=['GET', 'POST'])
##@login_required
#def web_origem():
#  from blueprints.igee.models import origem as origem_model
#  origens = origem_model.query.all()
#  form = NovaOrigemForm()
#  if form.validate_on_submit():
#    origem_object = origem_model(desc=form.desc.data)
#    origem_object.desc = form.desc.data
#    try:
#      db.session.add(origem_object)
#      db.session.commit()
#      flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(origem_object)), 'success')
#    except Exception as e:
#      db.session.rollback()
#      db.session.remove()
#      flash(u"Deu adubo! O problema foi o seguinte: %s" % (str(e)), 'danger')
#    return redirect(url_for('web_origem'))
#  return render_template('banco_simples.html', title=u"Busca de origens no banco", form=form, dados=origens)

### TODO API para banco de dados temporária

##from blueprints.api import bp
##from app import db
##from flask_login import login_required
##from flask import render_template, redirect, url_for, flash, request

#@bp.route('/db_origem', methods=['GET', 'POST'])
#@bp.route('/db_origem/<origem>', methods=['GET', 'POST'])
#@login_required
#def db_origem(origem=None):
#  from blueprints.api.models import igee_origem_v3 as origem_model
#  if origem is not None:
#    origem_object = origem_model.query.filter_by(desc=origem)
#  else:
#    origem_object = origem_model.query.all()
#  form = NovaOrigemForm()
#  if form.validate_on_submit():
#    uuid = great_uuid.uuid_string('origem', form.desc.data)
#    origem_nova = origem_model(uuid=uuid, desc=form.desc.data)
#    db.session.add(origem_nova)
#    db.session.commit()
#    flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(origem_nova)), 'success')
#    return redirect(url_for('db_origem', origem=origem_nova.desc))
#  return render_template('banco.html', title=u"Great Database - Origem", dados=origem_object, form=form)

#@bp.route('/db_origem_v3', methods=['GET', 'POST'])
#@bp.route('/db_origem_v3/<origem>', methods=['GET', 'POST'])
#@login_required
#def db_origem_v3(origem=None):
#  from blueprints.api.models import origem_v3 as origem_model
#  if origem is not None:
#    origem_object = origem_model.query.filter_by(desc=origem)
#  else:
#    origem_object = origem_model.query.all()
#  form = NovaOrigemForm()
#  if form.validate_on_submit():
#    uuid = great_uuid.uuid_string('origem_v3', form.desc.data)
#    origem_nova = origem_model(uuid=uuid, desc=form.desc.data)
#    db.session.add(origem_nova)
#    db.session.commit()
#    flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(origem_object)), 'success')
#    return redirect(url_for('db_origem_v3', origem=origem_nova.desc))
#  return render_template('banco.html', title=u"Great Database - Origem v3", dados=origem_object, form=form)

#@bp.route('/db_origem_add/<origem>', methods=['GET', 'POST'])
#@login_required
#def db_origem_add(origem):
#  from blueprints.api.models import igee_origem_v3 as origem_model
#  uuid = great_uuid.uuid_string('origem', origem)
#  origem_object = origem_model(uuid=uuid, desc=origem)
#  try:
#    db.session.add(origem_object)
#    db.session.commit()
#    flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(origem_object)), 'success')
#  except Exception as e:
#    db.session.rollback()
#    db.session.remove()
#    flash(u"Deu adubo! O problema foi o seguinte: %s" % (str(e)), 'danger')
#  return redirect(url_for('db_origem'))

### TODO API para banco de dados temporária
#@bp.route('/db_alimento', methods=['GET', 'POST'])
#@bp.route('/db_alimento/<alimento>', methods=['GET', 'POST'])
#@login_required
#def db_alimento(alimento=None):
#  from blueprints.igee.models import alimento_v3 as alimento_model, igee_v4 as igee_model
#  alimentos = list()
#  if alimento is not None:
#    alimento_object = alimento_model.query.get(alimento)
#  else:
#    alimento_objects = alimento_model.query.all()
#    for alimento_object in alimento_objects:
#      alimento_atual = dict()
#      alimento_atual['uuid'] = alimento_object.uuid
#      alimento_atual['timestamp'] = alimento_object.timestamp
#      alimento_atual['feedback'] = alimento_object.feedback
#      alimento_atual['igee'] = igee_model.query.get(alimento_object.uuid_igee).igee
#      alimentos.append(alimento_atual)
#  return render_template('alimentos.html', title=u"Great Database - Alimentos", dados=alimentos)



### Eat Raw

#from blueprints.eat import bp

#from blueprints.eat.models import funcionalidade as funcionalidade_model

##from flask import render_template, redirect, url_for, flash, request, session, abort
#from flask import render_template, request, redirect, url_for
##from flask_login import current_user, login_user, logout_user, login_required
#from flask_login import login_required

#import importlib
##from blueprints.eat.controllers.estoque import dados_estoque

#@bp.route('/')
##@login_required
#def index(aba=None):
#  funcionalidade_selecionada = funcionalidade_model(**{'label': u"Amor em Forma de Comida", 'icon': 'noun_forest_2784198', 'url': None, 'ordem': 0})
#  if len(request.args.getlist('aba')) > 0:
#    funcionalidade_object = funcionalidade_model.query.filter_by(url=request.args.getlist('aba')[0]).first()
#    if funcionalidade_object:
#      funcionalidade_selecionada = funcionalidade_object
#      funcionalidade_selecionada.selected = True
#  if funcionalidade_selecionada.url == None:
#    funcionalidade_selecionada.url = 'index'
#  funcionalidades_selecionadas = funcionalidade_model.query.order_by(funcionalidade_model.ordem).all()
#  if not len(funcionalidades_selecionadas) > 0:
#    funcionalidades_selecionadas = [funcionalidade_selecionada]
#  dados = dict()
#  ## TODO Essa é a hora em que o filho chora e a mãe não vê!
#  ## Ou este é o jeito mais inteligente de usar um método só pra todas as 
#  ## páginas, ou é a maior falha de segurança da história do Flask.
#  try:
#    ## Exemplo: para http://localhost:5000/?aba=estoque
#    ## from blueprints.eat.controllers.estoque import dados_estoque
#    ## dados = dados_estoque()
#    dados = getattr(
#      importlib.import_module(
#        '.'.join([
#          'blueprints',
#          'eat',
#          'controllers',
#          request.args.getlist('aba')[0]
#        ])
#      ),
#      '_'.join([
#        u"dados",
#        request.args.getlist('aba')[0]
#      ])
#    )()
#  except AttributeError as e:
#    print(u"[DEBUG] AttributeError: %s" % (e))
#    pass
#  except ImportError as e:
#    print(u"[DEBUG] ImportError: %s" % (e))
#    pass
#  except IndexError as e:
#    dados = dict()
#    print(u"[DEBUG] IndexError: %s" % (e))
#    pass
#  except Exception as e:
#    print(u"[DEBUG] Exception: %s" % (e))
#    raise
#  return render_template('.'.join([funcionalidade_selecionada.url, 'html']), title=funcionalidade_selecionada.label, funcionalidades=funcionalidades_selecionadas, dados=dados)

### TODO importar funcionalidades sem banco (precisa refazer todo o index)
##from copy import deepcopy
##from collections import OrderedDict
#### https://stackoverflow.com/a/13470505/11736767
##funcionalidades = OrderedDict(sorted(funcionalidades_mvp.items(), key=lambda k_v: k_v[1]['ordem']))
##funcionalidades_banco = funcionalidade_model.query.order_by(funcionalidade_model.ordem).all()



### Green Mapa Verde

#@bp.route('/')
##@login_required
#def index():
#  ## TODO Empresas fictícias
#  lojas = [
#    {
#      'id': 0,
#      'nome': 'vilaflores',
#      'desc': u"Vila Flores",
#      'lat': -30.018663,
#      'lng': -51.210258,
#      'icon': 'leaf-green.png',
#      'bg': 'green',
#    },
#    {
#      'id': 1,
#      'nome': 'fabricadofuturo',
#      'desc': u"Fábrica do Futuro",
#      'lat': -30.018600,
#      'lng': -51.207300,
#      'icon': 'leaf-red.png',
#      'bg': 'red',
#    },
#    {
#      'id': 2,
#      'nome': 'algumlugar',
#      'desc': u"Algum Lugar",
#      'lat': -30.0184,
#      'lng': -51.212,
#      'icon': 'leaf-orange.png',
#      'bg': 'purple',
#    },
#    {
#      'id': 3,
#      'nome': 'outrolugar',
#      'desc': u"Outro Lugar",
#      'lat': -30.0183,
#      'lng': -51.211,
#      'icon': 'leaf-orange.png',
#      'bg': 'blue',
#    },
#  ]
#  return render_template('index.html', title=u"Hoje é um Great Dia", lojas=lojas)

##@app.route('/web_ponto', methods=['GET', 'POST'])
###@login_required
##def web_ponto():
##  pontos = ponto_model.query.all()
##  form = NovoPontoForm()
##  if form.validate_on_submit():
##    ponto_object = ponto_model(lat=form.lat.data, lng=form.lng.data)
##    ponto_object.ponto = form.ponto.data
##    ponto_object.nome = form.nome.data
##    try:
##      db.session.add(ponto_object)
##      db.session.commit()
##      flash(u"Deu certo, Fortaleza! Dados inseridos: %s" % (str(ponto_object)), 'success')
##    except Exception as e:
##      db.session.rollback()
##      db.session.remove()
##      flash(u"Deu adubo! O problema foi o seguinte: %s" % (str(e)), 'danger')
##    return redirect(url_for('web_ponto'))
##  return render_template('ponto.html', title=u"Busca de pontos no banco", form=form, dados=pontos)




