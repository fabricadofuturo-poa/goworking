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
## Login / Registro

from datetime import datetime

from flask import (
  abort,
  flash,
  redirect,
  render_template,
  request,
  url_for,
)

from flask_login import current_user
#from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from urllib.parse import urlparse
from urllib.parse import urljoin

from app import (
  db,
  login_manager,
  logging,
)

from blueprints.goworking import bp

from blueprints.goworking.models import User

from blueprints.goworking.controllers import (
  LoginForm,
  SignupForm,
  custom_uuid,
)

from werkzeug.security import (
  generate_password_hash,
  check_password_hash,
)

#import os
#import sys
#sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

## https://github.com/
## fengsp/flask-snippets/blob/master/security/redirect_back.py
def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and \
    ref_url.netloc == test_url.netloc
def get_redirect_target():
  for target in request.values.get('next'), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return target
    else:
      return abort(400)
def redirect_back(endpoint, **values):
  target = request.form['next']
  if not target or not is_safe_url(target):
    target = url_for(endpoint, **values)
  return redirect(target)

@bp.route('/login', methods=['GET', 'POST'])
def login():
  # Bypass Login screen if user is logged in
  if current_user.is_authenticated:
    ## TODO Dar opção de logout / mudar conta
    flash(
      u"Vós já estais logada(o) como '%s'. Para desconectardes, acessai /logout"
      % (str(current_user.nome)),
      'warning',
    )
    return redirect(url_for('goworking.index'))
  # Here we use a class of some kind to represent and validate our
  # client-side form data. For example, WTForms is a library that will
  # handle this for us, and we use a custom LoginForm to validate.
  form = LoginForm()
  # POST: Create user and redirect them to the app
  if request.method == 'POST':
    if form.validate_on_submit():
      # Get Form Fields
      username = form.username.data
      password = form.password.data
      ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#      pronome = form.pronome.data
      # Validate Login Attempt
      # Login and validate the user.
      # user should be an instance of your `User` class
      user = User.query.filter_by(username=username).first()
      if user:
        if user.check_password(password=password):
          login_user(user, remember=form.remember_me.data)
          try:
            ## Agora
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()
          except Exception as e:
            logging.exception(e)
            db.session.rollback()
          flash(
            u"Olá %s" % (
              ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#              str(user.pronome),
              str(user.nome),
            ),
            'info',
          )
          ## There are actually three possible cases that need to be considered 
          ## to determine where to redirect after a successful login:
          ## If the login URL does not have a next argument, then the user is 
          ## redirected to the index page.
          ## If the login URL includes a next argument that is set to a 
          ## relative path (or in other words, a URL without the domain 
          ## portion), then the user is redirected to that URL.
          ## If the login URL includes a next argument that is set to a full 
          ## URL that includes a domain name, then the user is redirected to 
          ## the index page.
          ## The first and second cases are self-explanatory. The third case is 
          ## in place to make the application more secure. An attacker could 
          ## insert a URL to a malicious site in the next argument, so the 
          ## application only redirects when the URL is relative, which ensures 
          ## that the redirect stays within the same site as the application. 
          ## To determine if the URL is relative or absolute, I parse it with 
          ## Werkzeug's url_parse() function and then check if the netloc 
          ## component is set or not.
          ## TODO tá ruim
#          next = get_redirect_target()
#          return redirect_back('goworking.index')
          next_page = request.args.get('next')
          if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('goworking.index')
          return redirect(next_page)
        else:
          flash(
            u"Senha errada!",
            'danger',
          )
          return redirect(url_for('goworking.login'))
      else: # user = None
        flash(
          u"Não encontramos '%s' :( Tens certeza de que é assim mesmo que se \
          escreve? Por favor tente novamente. Se o erro foi meu, então peço \
          desculpas :@"
          % (str(form.username.data)),
          'danger',
        )
        return redirect(url_for('goworking.login'))
  # GET: Serve Log-in page
  return render_template(
    'login.html',
    form=form,
    title=u"Login",
  )

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    ## TODO Dar opção de logout / mudar conta
    flash(
      u"Vós já estais logada(o) como '%s'. Para desconectardes, acessai /logout"
      % (str(current_user.nome)),
      'warning',
    )
    return redirect(url_for('goworking.index'))
  form = SignupForm()
  # POST: Sign user in
  if request.method == 'POST':
    if form.validate_on_submit():
      # Get Form Fields
      username = form.username.data
      existing_user = User.query.filter_by(username=username).first()
      if existing_user is not None:
        flash(
          u"O nome de usuário '%s' já existe! Escolha outro."
          % (form.username.data),
          'warning',
        )
        return redirect(url_for('goworking.signup'))
      password = form.password.data
      nome = form.nome.data
      ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#      pronome = form.pronome.data
      ## Gera um uuid aleatório até que não exista nenhum idêntico no banco de 
      ## dados. Mesmo que a chance hipotética de ter seja altamente improvável.
      id = custom_uuid.random_uuid()
      while User.query.filter_by(id=id).first():
        id = custom_uuid.random_uuid()
      ## Agora
      created_on = datetime.utcnow()
      try:
        user = User(
          id = id,
          username = username,
          password = generate_password_hash(password, method='sha256'),
          nome = nome,
          ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#          pronome = pronome,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(
          u"Olá %s" % (
          ## TODO A Marta disse que vai contra nova cartilha de etiqueta de comunicação
#            str(form.pronome.data),
            str(form.nome.data)
          ),
          'info',
        )
        ## TODO tá ruim
#        next = get_redirect_target()
#        return redirect_back('goworking.index')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
          next_page = url_for('goworking.index')
        return redirect(next_page)
      except Exception as e:
        logging.exception(e)
        db.session.rollback()
        db.session.remove()
        flash(
          u"Não deu certo! O problema foi o seguinte: %s"
          % (str(e)),
          'danger',
        )
  # GET: Serve Sign-up page
  return render_template(
    'signup.html',
    title=u"Registre-se",
    form=form,
  )

@bp.route('/logout')
def logout():
  logout_user()
  flash(u"Volte sempre! ;)", 'primary')
  return redirect(url_for('goworking.index'))

