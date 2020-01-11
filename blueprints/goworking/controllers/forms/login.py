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

from app import db

## WTF
from flask_wtf import FlaskForm
from wtforms import (
  BooleanField,
  HiddenField,
  PasswordField,
  RadioField,
  StringField,
  SubmitField,
#  TextAreaField,
#  TextField,
)
from wtforms.validators import (
  DataRequired,
  EqualTo,
  Length,
  Regexp,
#  ValidationError,
)
from wtforms_validators import Alpha
#from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
  username = StringField(
    u"Login",
    validators = [
      DataRequired(message = u"Somente letras, tudojuntoeminusculo. \
        Não tem login ainda? Clique em 'Registrar' lá embaixo!"),
      Alpha(message = u"Somente letras, tudojuntoeminusculo"),
    ],
    description='jocimara',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Somente letras, \
        tudojuntoeminusculo. Não tem login ainda? Clique em \'Registrar\' lá \
        embaixo!");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  password = PasswordField(
    u"Senha",
    validators = [
      DataRequired(message = u"Qual é a senha?"),
    ],
    description='********',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Qual é a senha?");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  mr_robot = BooleanField(
    u"Eu não sou um robô",
    validators=[DataRequired(message=(u"Não autenticamos robôs por este \
      formulário, favor marcar esta opção."),),],
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Não autenticamos robôs por este \
        formulário, favor marcar esta opção.");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  remember_me = BooleanField(u"Lembrar de mim")
  submit = SubmitField(u"Entrar")

class SignupForm(FlaskForm):
  username = StringField(
    u"Login",
    validators = [
      DataRequired(message = u"Login é necessário e tu precisa decorar, assim \
        como a senha."),
      Alpha(message = u"Somente letras, tudojuntoeminusculo"),
    ],
    description='jocimara',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Somente letras, \
        tudojuntoeminusculo. Não tem login ainda? Clique em \'Registrar\' lá \
        embaixo!");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  password = PasswordField(
    u"Senha",
    validators = [
      DataRequired(message = u"Senha é necessária e tu precisa decorar."),
      Length(
        min=3,
        message = u"A senha precisa ter pelo menos 3 (três) caracteres.",
      ),
      EqualTo('confirm', message=u"As duas senhas na verdade são a mesma!",),
    ],
    description='********',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Qual é a senha?");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  confirm = PasswordField(
    u"Senha de novo",
    validators = [
      DataRequired(message = u"É a mesma senha de novo!"),
      Length(
        min=3,
        message = u"A senha tinha que ter pelo menos 3 (três) caracteres.",
      ),
    ],
    description='********',
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Qual é a senha de novo?");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  nome = StringField(
    u"Nome",
    validators=[DataRequired(message = u"Qual é o teu nome?")],
    description=u"Jocimara da Silva dos Santos",
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Qual é o teu nome?");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#  pronomes = [
#    ('a', u"Bem vind<b>a</b>"),
#    ('o', u"Bem vind<b>o</b>"),
#    ('e', u"Bem vind<b>e</b>"),
#    ('s', u"Bem vind<b>s</b>"),
#    ('x', u"Bem vind<b>x</b>"),
#    ('@', u"Bem vind<b>@</b>"),
#    ('is', u"Bem vind<b>is</b>, cacilds"),
#  ]
#  pronome = RadioField(u"Como eu te cumprimento?", choices=pronomes)
  pronome = HiddenField()
  mr_robot = BooleanField(
    u"Eu não sou um robô",
    validators=[DataRequired(message=(u"Não autenticamos robôs por este \
      formulário, favor marcar esta opção."),),],
    render_kw=({
      'oninvalid': 'this.setCustomValidity("Não autenticamos robôs por este \
        formulário, favor marcar esta opção.");',
      'oninput': 'this.setCustomValidity("");',
    }),
  )
  submit = SubmitField(u"Registrar")

