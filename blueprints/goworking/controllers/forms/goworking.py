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

## WTF
from flask_wtf import FlaskForm
from wtforms import (
  BooleanField,
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

ordens_cadeiras = [
  (0, u"A"),
  (1, u"B"),
  (2, u"C"),
  (3, u"D"),
]

ordens_mesas = [
  (0, u"0 (auditório)"),
  (1, u"1 (jardim)"),
  (2, u"2 (jardim)"),
  (3, u"3 (jardim"),
  (4, u"4 (auditório)"),
  (5, u"5 (auditório)"),
  (6, u"6"),
  (7, u"7"),
  (8, u"8 (auditório)"),
  (9, u"9 (auditório)"),
  (10, u"10"),
  (11, u"11"),
  (12, u"12 (corredor)"),
  (13, u"13 (corredor)"),
  (14, u"14"),
  (15, u"15"),
  (16, u"16 (banheiro masculino)"),
  (17, u"17 (banheiro chuveiros)"),
  (18, u"18"),
  (19, u"19"),
  (20, u"20 (banheiro feminino)"),
  (21, u"21 (banheiro pcd)"),
  (22, u"22"),
  (23, u"23"),
  (24, u"24 (banheiro feminino)"),
  (25, u"25 (corredor parede grafitada)"),
  (26, u"26"),
  (27, u"27"),
  (28, u"28"),
  (29, u"29"),
  (30, u"30"),
  (31, u"31"),
  (32, u"32"),
  (33, u"33"),
  (34, u"34"),
  (35, u"35"),
  (36, u"36 (sala de reuniões)"),
  (37, u"37 (sala de reuniões)"),
  (38, u"38 (televisão)"),
  (39, u"39 (recepção)"),
]

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

class NovaEspacoForm(FlaskForm):
  numero = StringField(
    u"Número",
    validators = [
      DataRequired(message = u"Exemplo: 01 para o espaço 01"),
    ],
    description = 'Exemplo: 01 para o espaço 01',
    render_kw = ({
      'oninvalid': 'this.setCustomValidity("Exemplo: 01 para o espaço \
        01");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  desc = TextAreaField(
    u"Descrição",
    description = u"Escreva o que quiser sobre o espaço aqui, depois a \
      gente vai organizando em outros campos conforme a necessidade ;)",
    validators = [Optional()],
    render_kw=({
      'rows': '6',
      'cols': '45',
    }),
  )
  ordem = SelectField(
    u"Posição do espaço no goworking",
    coerce = int,
    choices = ordens_mesas,
    render_kw = ({'class': 'form-group'})
  )
  submit = SubmitField(
    u"Cadastrar",
    render_kw = ({'class': 'btn btn-primary'}),
  )

class EditarEspacoForm(NovaEspacoForm):
  id = StringField(widget = HiddenInput())
  submit = SubmitField(
    u"Atualizar",
    render_kw = ({'class': 'btn btn-info'}),
  )

class NovaMesaForm(FlaskForm):
  numero = StringField(
    u"Número",
    validators = [
      DataRequired(message = u"Exemplo: 01 para a mesa 01"),
    ],
    description = 'Exemplo: 01 para a mesa 01',
    render_kw = ({
      'oninvalid': 'this.setCustomValidity("Exemplo: 01 para a mesa \
        01");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  desc = TextAreaField(
    u"Descrição",
    description = u"Escreva o que quiser sobre a mesa aqui, depois a \
      gente vai organizando em outros campos conforme a necessidade ;)",
    validators = [Optional()],
    render_kw=({
      'rows': '6',
      'cols': '45',
    }),
  )
  id_espaco = QuerySelectField(
    u"Espaço",
    query_factory = espacos,
    allow_blank = False,
    get_label = 'numero',
    blank_text = u"Selecione um Espaço...",
    validators = [
      DataRequired(message = u"Selecione um Espaço. Não tem nenhum? \
      Cadastre!"),
    ],
    render_kw = ({
      'oninvalid': 'this.setCustomValidity("Selecione um Espaço. Não \
        tem nenhum? Cadastre!");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  ordem = SelectField(
    u"Posição da mesa no goworking",
    coerce=int,
    choices=ordens_mesas,
    render_kw=({'class': 'form-group'})
  )
  submit = SubmitField(
    u"Cadastrar",
    render_kw = ({'class': 'btn btn-primary'}),
  )

class EditarMesaForm(NovaMesaForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(
    u"Atualizar",
    render_kw = ({'class': 'btn btn-info'}),
  )

class NovaCadeiraForm(FlaskForm):
  numero = StringField(
    u"Número",
    validators = [
      DataRequired(message = u"Exemplo: 01-A para a cadeira A da mesa \
        01"),
    ],
    description = 'Exemplo: 01-A para a cadeira A da mesa 01',
    render_kw = ({
      'oninvalid': 'this.setCustomValidity("Exemplo: 01-A para a \
        cadeira A da mesa 01");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  ordem = RadioField(
    u"Posição da cadeira no goworking",
    coerce = int,
    choices = ordens_cadeiras,
    render_kw = ({'class': 'form-group'})
  )
  desc = TextAreaField(
    u"Descrição",
    description = u"Escreva o que quiser sobre a cadeira aqui, depois \
      a gente vai organizando em outros campos conforme a necessidade \
      ;)",
    validators = [Optional()],
    render_kw = ({
      'rows': '6',
      'cols': '45',
    }),
  )
  id_mesa = QuerySelectField(
    u"Mesa",
    query_factory = mesas,
    allow_blank = False,
    get_label = 'numero',
    blank_text = u"Selecione uma Mesa...",
    validators = [
      DataRequired(message = u"Selecione uma Mesa. Não tem nenhuma? \
      Cadastre!"),
    ],
    render_kw = ({
      'oninvalid': 'this.setCustomValidity("Selecione uma Mesa. Não \
          tem nenhuma? Cadastre!");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  submit = SubmitField(
    u"Cadastrar",
    render_kw = ({'class': 'btn btn-primary'}),
  )

class EditarCadeiraForm(NovaCadeiraForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(
    u"Atualizar",
    render_kw = ({'class': 'btn btn-info'}),
  )

class NovaEmpresaForm(FlaskForm):
  nome = StringField(
    u"Nome",
    validators = [
      DataRequired(message = u"Faltou o Nome da Empresa"),
    ],
    description=u"Fábrica do Futuro",
    render_kw = ({
      'oninvalid':
        'this.setCustomValidity("Faltou o Nome da Empresa");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  cnpj = StringField(
    u"CNPJ",
    validators = [
      Optional(),
      Length(
        min = 14,
        max = 18,
        message = u"CNPJ tem 14 dígitos e 18 caracteres!",
      ),
      # ~ Integer(message = u"Somente números."),
    ],
    description=u"12345678901234",
  )
  desc = TextAreaField(
    u"Descrição",
    description = u"Escreva o que quiser sobre a empresa aqui, depois \
      a gente vai organizando em outros campos conforme a necessidade \
      ;)",
    validators = [Optional()],
    render_kw = ({
      'rows': '6',
      'cols': '45',
    }),
  )
  submit = SubmitField(
    u"Cadastrar",
    render_kw = ({'class': 'btn btn-primary'}),
  )

class EditarEmpresaForm(NovaEmpresaForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(
    u"Atualizar",
    render_kw = ({'class': 'btn btn-info'}),
  )
