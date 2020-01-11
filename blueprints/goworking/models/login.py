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
## Flask Login

from datetime import datetime

from app import db
from app import login_manager

from flask_login import UserMixin

from blueprints.goworking.controllers import custom_uuid

from werkzeug.security import (
  generate_password_hash,
  check_password_hash,
)

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(
    db.String(36),
    primary_key=True,
    unique=True,
    nullable=False,
    default=custom_uuid.random_uuid,
  )
  timestamp = db.Column(
    db.TIMESTAMP,
    index=True,
    default=datetime.utcnow,
  )
  nome = db.Column(
    db.String(255),
    unique=False,
    nullable=False,
  )
  pronome = db.Column(
    db.String(2),
    unique=False,
    nullable=True,
  )
  username = db.Column(
    db.String(255),
    unique=True,
    nullable=False,
  )
  password = db.Column(
    db.String(255),
    primary_key=False,
    unique=False,
    nullable=False,
  )
  created_on = db.Column(
    db.DateTime,
    index=False,
    unique=False,
    nullable=True,
    default=datetime.utcnow,
  )
  last_login = db.Column(
    db.DateTime,
    index=False,
    unique=False,
    nullable=True,
    default=datetime.utcnow,
  )

  def set_password(self, password):
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return """<User 'id: %s',
      'timestamp: %s',
      'nome: %s',
      'username: %s',
      'password: %s',
      'created_on: %s',
      'last_login: %s'>""" % (
      self.id,
      str(self.timestamp),
      self.nome,
      self.username,
      'eusoumuitoimbecil',
      str(self.created_on),
      str(self.last_login)
    )

