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

import datetime

## WTF
from flask_wtf import FlaskForm
from wtforms import (
  BooleanField,
  DateField,
  HiddenField,
  PasswordField,
  RadioField,
  SelectField,
  StringField,
  SubmitField,
  TextAreaField,
#  TextField,
)
from wtforms.validators import (
  DataRequired,
  EqualTo,
  Length,
  Optional,
  Regexp,
#  ValidationError,
)
from wtforms.widgets import HiddenInput
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_validators import (
  Alpha,
  Integer,
)

from app import db

from blueprints.goworking.models.goworking import (
  espaco as espaco_model,
  mesa as mesa_model,
  cadeira as cadeira_model,
  empresa as empresa_model,
  habitante as habitante_model,
)

def espacos():
  return espaco_model.query.order_by(espaco_model.numero)
def mesas():
  return mesa_model.query.order_by(mesa_model.numero)
def cadeiras():
  return cadeira_model.query.order_by(cadeira_model.numero)
def empresas():
  return empresa_model.query.order_by(empresa_model.nome)
def habitantes():
  return habitante_model.query.order_by(habitante_model.nome)

class NovaHabitanteForm(FlaskForm):
  nome = StringField(
    u"Nome",
    validators = [
      DataRequired(message = u"Faltou o Nome da Habitante"),
    ],
    description=u"Jocimara dos Santos",
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Faltou o Nome da Habitante");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  cpf = StringField(
    u"CPF",
    validators = [
      Optional(),
      #~ Length(11, message = u"CPF tem 11 dígitos!"),
      #~ Integer(message = u"Somente números."),
    ],
    description=u"12345678901",
  )
  desc = TextAreaField(
    u"Descrição",
    description=u"Escreva o que quiser sobre a(o) habitante aqui, depois a \
      gente vai organizando em outros campos conforme a necessidade ;)",
    validators = [Optional()],
    render_kw=({
      'rows': '6',
      'cols': '45',
    }),
  )
  data_entrada = DateField(
    u"Data de Entrada",
    validators = [
      Optional(),
    ],
    #~ format = '%d/%m/&Y',
    render_kw=({
      'type': 'date',
    }),
  )
  data_saida = DateField(
    u"Data de Saída",
    validators = [
      Optional(),
    ],
    #~ format = '%d/%m/&Y',
    render_kw=({
      'type': 'date',
    }),
  )
  data_renovacao = DateField(
    u"Data de Renovação",
    validators = [
      Optional(),
    ],
    #~ format = '%d/%m/&Y',
    render_kw=({
      'type': 'date',
    }),
  )
  empresa = QuerySelectField(
    u"Empresa",
    query_factory = empresas,
    get_label = 'nome',
    allow_blank = True,
    blank_text = u"Selecione uma Empresa...",
    validators = [Optional()],
  )
  cadeira = QuerySelectField(
    u"Cadeira",
    query_factory = cadeiras,
    get_label = 'numero',
    allow_blank = True,
    blank_text = u"Selecione uma Cadeira...",
    validators = [Optional()],
  )
  submit = SubmitField(u"Cadastrar", render_kw=({'class': 'btn btn-primary'}))

class EditarHabitanteForm(NovaHabitanteForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(u"Atualizar", render_kw=({'class': 'btn btn-info'}))
