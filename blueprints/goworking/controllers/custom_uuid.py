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
## Padroniza utilização local de UUID

import uuid

## NIL
nil_uuid = uuid.UUID('{00000000-0000-0000-0000-000000000000}')

default_string = 'fabricadofuturo'
default_uuid = nil_uuid

## UUID('6137e891-6c26-5e69-9676-4a00550ad64f')
custom_uuid = uuid.uuid5(default_uuid, default_string)

def uuid4_to_string():
  return str(uuid.uuid4())

def uuid5_to_string(namespace=custom_uuid, string=default_string):
  return str(uuid.uuid5(namespace, string))

## Retorna um UUID pseudo aleatório
def random_uuid():
  return uuid4_to_string()

## Gera um UUID replicável a partir de duas strings, sendo a primeira utilizada 
## para gerar um namespace usando o namespace NIL
def uuid_string(namespace=default_string, string=default_string):
  return uuid5_to_string(uuid.uuid5(default_uuid, namespace), string)
## Como o método anterior, mas recebe um UUID em forma de string
def uuid_namespace(namespace=default_uuid, string=default_string):
  return uuid5_to_string(uuid.UUID('{%s}' % (namespace)), string)

## Retorna um UUID replicável com o namespace customizado, ou o namespace 
## customizado em caso de ausência de parâmetros.
def custom_namespace():
  return custom_uuid
def custom_namespace(string):
  return uuid5_to_string(custom_uuid, string)

