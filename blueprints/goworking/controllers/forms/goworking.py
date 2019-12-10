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
  mesa as mesa_model,
  cadeira as cadeira_model,
  empresa as empresa_model,
  habitante as habitante_model,
)

ordens_cadeiras = [
  (1, u"A"),
  (2, u"B"),
  (3, u"C"),
  (4, u"D"),
]

ordens_mesas = [
  ('-3', u"-3 (auditório)"),
  ('-2', u"-2 (jardim)"),
  ('-1', u"-1 (jardim)"),
  ('0', u"0 (jardim"),
  ('1', u"1 (auditório)"),
  ('2', u"2 (auditório)"),
  ('3', u"3"),
  ('4', u"4"),
  ('5', u"5 (auditório)"),
  ('6', u"6 (auditório)"),
  ('7', u"7"),
  ('8', u"8"),
  ('9', u"9 (corredor)"),
  ('10', u"10 (corredor)"),
  ('11', u"11"),
  ('12', u"12"),
  ('13', u"13 (banheiro masculino)"),
  ('14', u"14 (banheiro chuveiros)"),
  ('15', u"15"),
  ('16,' u"16"),
  ('17', u"17 (banheiro feminino)"),
  ('18', u"18 (banheiro pcd)"),
  ('19', u"19"),
  ('20', u"20"),
  ('21', u"21 (banheiro feminino)"),
  ('22', u"22 (corredor parede grafitada)"),
  ('23', u"23"),
  ('24', u"24"),
  ('25', u"25"),
  ('26', u"26"),
  ('27', u"27"),
  ('28', u"28"),
  ('29', u"29"),
  ('30', u"30"),
  ('31', u"31"),
  ('32', u"32"),
]

def mesas():
  return db.session.query(mesa_model).all()
def cadeiras():
  return db.session.query(cadeira_model).all()
def empresas():
  return db.session.query(empresa_model).all()
def habitantes():
  return db.session.query(habitante_model).all()

class NovaMesaForm(FlaskForm):
  numero = StringField(
    u"Número - Exemplo: 01 para a mesa 01",
    validators = [
      DataRequired(message = u"Exemplo: 01 para a mesa 01"),
    ],
    description='01',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Exemplo: 01 para a mesa 01");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  ordem = SelectField(u"Posição da mesa no go working", coerce=int, choices=ordens_mesas)
  submit = SubmitField(u"Cadastrar / Atualizar")

class EditarMesaForm(NovaMesaForm):
  id = StringField(widget=HiddenInput())

class NovaCadeiraForm(FlaskForm):
  numero = StringField(
    u"Número - Exemplo: 01-A para a cadeira A da mesa 01",
    validators = [
      DataRequired(message = u"Exemplo: 01-A para a cadeira A da mesa 01"),
    ],
    description='01-A',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Exemplo: 01-A para a cadeira A da \
        mesa 01");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  ordem = RadioField(u"Posição da cadeira", coerce=int, choices=ordens_cadeiras)
  id_mesa = QuerySelectField(
    u"Mesa",
    query_factory=mesas,
    allow_blank=False,
    get_label='numero',
    get_pk=lambda a: a.id,
    blank_text=u"Selecione uma Mesa...",
    validators=[DataRequired(message = u"Selecione uma Mesa. Não tem nenhuma? \
      Cadastre!")],
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Selecione uma Mesa. Não tem \
        nenhuma? Cadastre!");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  submit = SubmitField(u"Cadastrar / Atualizar")

class EditarCadeiraForm(NovaCadeiraForm):
  id = StringField(widget=HiddenInput())

class NovaEmpresaForm(FlaskForm):
  nome = StringField(
    u"Nome",
    validators = [
      DataRequired(message = u"Faltou o Nome da Empresa"),
    ],
    description=u"Fábrica do Futuro",
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Faltou o Nome da Empresa");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  cnpj = StringField(
    u"CNPJ",
    validators = [
      Optional(),
      Length(14, message = u"CNPJ tem 14 dígitos!"),
      Integer(message = u"Somente números."),
    ],
    description=u"12345678901234",
  )
  desc = TextAreaField(
    u"Descrição",
    description=u"Escreva o que quiser sobre a empresa aqui, depois a gente vai organizando em outros campos conforme a necessidade ;)",
    validators = [Optional()],
    render_kw=({
      'rows': '6',
      'cols': '45',
    }),
  )
  submit = SubmitField(u"Cadastrar", render_kw=({'class': 'btn btn-primary'}))

class EditarEmpresaForm(NovaEmpresaForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(u"Atualizar", render_kw=({'class': 'btn btn-info'}))

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
      Length(11, message = u"CPF tem 11 dígitos!"),
      Integer(message = u"Somente números."),
    ],
    description=u"12345678901",
  )
  desc = TextAreaField(
    u"Descrição",
    description=u"Escreva o que quiser sobre a(o) habitante aqui, depois a gente vai organizando em outros campos conforme a necessidade ;)",
    validators = [Optional()],
    render_kw=({
      'rows': '6',
      'cols': '45',
    }),
  )
  id_empresa = QuerySelectField(
    u"Empresa",
    query_factory=empresas,
    allow_blank=True,
    get_label='nome',
    get_pk=lambda a: a.id,
    blank_text=u"Selecione uma Empresa...",
    validators = [Optional()],
  )
  id_cadeira = QuerySelectField(
    u"Cadeira",
    query_factory=cadeiras,
    allow_blank=True,
    get_label='numero',
    get_pk=lambda a: a.id,
    blank_text=u"Selecione uma Cadeira...",
    validators = [Optional()],
  )
  submit = SubmitField(u"Cadastrar", render_kw=({'class': 'btn btn-primary'}))

class EditarHabitanteForm(NovaHabitanteForm):
  id = StringField(widget=HiddenInput())
  submit = SubmitField(u"Atualizar", render_kw=({'class': 'btn btn-info'}))

