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
## Preenche banco de dados com dados iniciais

from app import db
from blueprints.goworking.controllers import custom_uuid
from blueprints.goworking.controllers.db.dummy import goworking_esqueleto
from blueprints.goworking.models import (
  espaco as espaco_model,
  mesa as mesa_model,
  cadeira as cadeira_model,
)

def popular_espacos():
  filas = goworking_esqueleto()
  for fila in filas:
    for coluna in fila['colunas']:
      ## Cria novo espaço
      id = custom_uuid.random_uuid()
      while espaco_model.query.filter_by(id=id).first():
        id = custom_uuid.random_uuid()
      espaco_novo = espaco_model(
        id = id,
        ordem = int(coluna['ordem']),
        numero = str(coluna['ordem']),
        desc = coluna['desc'],
      )
      if not espaco_model.query.filter_by(
        ordem = espaco_novo.ordem,
      ).first():
        print(u"Adicionando espaço novo: %s" % (espaco_novo))
        db.session.add(espaco_novo)
        try:
          db.session.commit()
        except Exception as e:
          print(u"[ERRO]: %s" % (e))
      else:
        print(u"Espaço já existe: %s" % (espaco_novo))

def popular_mesas():
  ## Cadeira "nenhuma"
  id = custom_uuid.random_uuid()
  while cadeira_model.query.filter_by(id=id).first():
    id = custom_uuid.random_uuid()
  cadeira_nova = cadeira_model(id = id, numero = 'NADA')
  if not cadeira_model.query.filter_by(
    numero = cadeira_nova.numero,
  ).first():
    print(u"Adicionando cadeira nova: %s" % 
    (cadeira_nova))
    db.session.add(cadeira_nova)
  else:
    print(u"Cadeira já existe: %s" % (cadeira_nova))
  filas = goworking_esqueleto()
  espacos = espaco_model.query.all()
  for fila in filas:
    for coluna in fila['colunas']:
      if 'numero' in coluna:
        ## Cria nova mesa
        id = custom_uuid.random_uuid()
        while mesa_model.query.filter_by(id=id).first():
          id = custom_uuid.random_uuid()
        id_espaco = next((
          espaco.id
          for espaco in espacos
          if espaco.ordem == coluna['ordem']
        ), None)
        if id_espaco and coluna['id_mesa']:
          mesa_nova = mesa_model(
            id = id,
            ordem = int(coluna['ordem']),
            numero = "{:02d}".format(coluna['numero']),
            desc = coluna['desc'],
            id_espaco = id_espaco,
          )
          if not mesa_model.query.filter_by(
            numero = mesa_nova.numero,
          ).first():
            print(u"Adicionando mesa nova: %s" % (mesa_nova))
            db.session.add(mesa_nova)
            mapa = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
            for ordem in range(0, 4):
              id = custom_uuid.random_uuid()
              while cadeira_model.query.filter_by(id=id).first():
                id = custom_uuid.random_uuid()
              cadeira_nova = cadeira_model(
                id = id,
                ordem = ordem,
                numero = '-'.join([
                  "{:02d}".format(coluna['numero']),
                  mapa[ordem],
                ]),
                id_mesa = mesa_nova.id,
              )
              if not cadeira_model.query.filter_by(
                numero = cadeira_nova.numero,
              ).first():
                print(u"Adicionando cadeira nova: %s" % 
                (cadeira_nova))
                db.session.add(cadeira_nova)
              else:
                print(u"Cadeira já existe: %s" % (cadeira_nova))
          else:
            print(u"Mesa já existe: %s" % (mesa_nova))
      else:
        print(u"Espaço não tinha mesa: %s" % (coluna))
      try:
        db.session.commit()
        pass
      except Exception as e:
        print(u"[ERRO]: %s" % (e))
