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

import datetime, json

from blueprints.goworking.controllers import custom_uuid

def dados_mesas():
  dados = {
    'mesas': list(),
    'cadeiras': list(),
    'pessoas': list(),
    'empresas': list(),
    }
  
  ## TODO fictício
  dados['mesas'] = [
    {
      'id': '00',
      'numero': 0,
    },
    {
      'id': '01',
      'numero': 1,
    },
    {
      'id': '02',
      'numero': 2,
    },
    {
      'id': '03',
      'numero': 3,
    },
    {
      'id': '04',
      'numero': 4,
    },
    {
      'id': '05',
      'numero': 5,
    },
    {
      'id': '06',
      'numero': 6,
    },
    {
      'id': '07',
      'numero': 7,
    },
    {
      'id': '08',
      'numero': 8,
    },
    {
      'id': '09',
      'numero': 9,
    },
    {
      'id': '10',
      'numero': 10,
    },
    {
      'id': '11',
      'numero': 11,
    },
    {
      'id': '12',
      'numero': 12,
    },
    {
      'id': '13',
      'numero': 13,
    },
    {
      'id': '14',
      'numero': 14,
    },
    {
      'id': '15',
      'numero': 15,
    },
    {
      'id': '16',
      'numero': 16,
    },
    {
      'id': '17',
      'numero': 17,
    },
    {
      'id': '18',
      'numero': 18,
    },
    {
      'id': '19',
      'numero': 19,
    },
    {
      'id': '20',
      'numero': 20,
    },
  ]
  dados['cadeiras'] = [
    {
      'id': '21',
      'desc': u"Nenhuma",
      'id_mesa': '00',
    },
    {
      'id': '22',
      'desc': u"01-B",
      'id_mesa': '01',
    },
    {
      'id': '23',
      'desc': u"01-C",
      'id_mesa': '01',
    },
    {
      'id': '24',
      'desc': u"01-D",
      'id_mesa': '01',
    },
    {
      'id': '25',
      'desc': u"02-A",
      'id_mesa': '02',
    },
    {
      'id': '26',
      'desc': u"02-B",
      'id_mesa': '02',
    },
    {
      'id': '27',
      'desc': u"02-C",
      'id_mesa': '02',
    },
    {
      'id': '28',
      'desc': u"02-D",
      'id_mesa': '02',
    },
    {
      'id': '29',
      'desc': u"03-A",
      'id_mesa': '03',
    },
  ]
  dados['empresas'] = [
    {
      'id': '30',
      'nome': u"Nenhuma",
      'cnpj': '0000000000000000',
    },
    {
      'id': '31',
      'nome': u"Fábrica do Futuro",
      'cnpj': '0000100020003000',
    },
  ]
  dados['pessoas'] = [
    {
      'id': '33',
      'nome': u"Ninguém",
      'id_empresa': '30',
      'id_mesa': '00',
      'id_cadeira': '21',
      'data_entrada': datetime.datetime(1, 1, 1, 0, 0),
      'data_saida': datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
      'data_renovacao': datetime.datetime(1, 1, 1, 0, 0),
    },
    {
      'id': '32',
      'nome': u"Iuri Guilherme",
      'id_empresa': '31',
      'id_mesa': '01',
      'id_cadeira': '22',
      'data_entrada': datetime.datetime(1, 1, 1, 0, 0),
      'data_saida': datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
      'data_renovacao': datetime.datetime(2019, 8, 19, 20, 52, 52, 460036),
    },
  ]
  
  for mesa in dados['mesas']:
    mesa['cadeiras'] = [
      {
        'id': cadeira['id'],
        'id_mesa': cadeira['id_mesa'],
        'desc': cadeira['desc'],
      }
      for cadeira in dados['cadeiras']
      if cadeira['id_mesa'] == mesa['id']
    ]
    for cadeira in mesa['cadeiras']:
      cadeira['pessoa'] = next(
        (
          {
            'id': pessoa['id'],
            'nome': pessoa['nome'],
            'id_mesa': pessoa['id_mesa'],
            'id_cadeira': pessoa['id_cadeira'],
            'id_empresa': pessoa['id_empresa'],
            'data_entrada': pessoa['data_entrada'],
            'data_saida': pessoa['data_saida'],
            'data_renovacao': pessoa['data_renovacao'],
          }
          for pessoa in dados['pessoas']
          if pessoa['id_cadeira'] == cadeira['id']
        ),
        {
          'id': '33',
          'nome': u"Ninguém",
          'id_mesa': '00',
          'id_cadeira': '21',
          'id_empresa': '30',
          'data_entrada': datetime.datetime.min,
          'data_saida': datetime.datetime.max,
          'data_renovacao': datetime.datetime.utcnow(),
        }
      )
      cadeira['pessoa']['nome'] = next(
        (
          pessoa['nome']
          for pessoa in dados['pessoas']
          if pessoa['id'] == cadeira['pessoa']['id']
        ),
        u"Ninguém"
      )
      cadeira['pessoa']['data_entrada'] = next(
        (
          pessoa['data_entrada']
          for pessoa in dados['pessoas']
          if pessoa['id'] == cadeira['pessoa']['id']
        ),
        datetime.datetime.min
      )
      cadeira['pessoa']['data_saida'] = next(
        (
          pessoa['data_saida']
          for pessoa in dados['pessoas']
          if pessoa['id'] == cadeira['pessoa']['id']
        ),
        datetime.datetime.max
      )
      cadeira['pessoa']['data_renovacao'] = next(
        (
          pessoa['data_renovacao']
          for pessoa in dados['pessoas']
          if pessoa['id'] == cadeira['pessoa']['id']
        ),
        datetime.datetime.utcnow()
      )
      cadeira['pessoa']['empresas'] = [
        {
          'id': empresa['id'],
          'nome': empresa['nome'],
          'cnpj': empresa['cnpj']
        }
        for empresa in dados['empresas']
        if empresa['id'] == cadeira['pessoa']['id_empresa']
      ]
  
  return dados['mesas']

#  "mesas": [
#    {
#      "id": "00",
#      "numero": 0,
#      "cadeiras": [
#        {
#          "desc": "Nenhuma",
#          "id": "21",
#          "id_mesa": "00",
#          "pessoa": {
#            "data_entrada": "0001-01-01 00:00:00",
#            "data_renovacao": "0001-01-01 00:00:00",
#            "data_saida": "9999-12-31 23:59:59.999999",
#            "empresas": [
#              {
#                "cnpj": "0000000000000000",
#                "id": "30",
#                "nome": "Nenhuma"
#              }
#            ],
#            "id": "33",
#            "id_cadeira": "21",
#            "id_empresa": "30",
#            "id_mesa": "00",
#            "nome": "Ningu\u00e9m"
#          }
#        }
#      ],
#    },
#    {
#      "id": "01",
#      "numero": 1
#      "cadeiras": [
#        {
#          "desc": "01-B",
#          "id": "22",
#          "id_mesa": "01",
#          "pessoa": {
#            "data_entrada": "0001-01-01 00:00:00",
#            "data_renovacao": "2019-08-19 20:52:52.460036",
#            "data_saida": "9999-12-31 23:59:59.999999",
#            "empresas": [
#              {
#                "cnpj": "0000100020003000",
#                "id": "31",
#                "nome": "F\u00e1brica do Futuro"
#              }
#            ],
#            "id": "32",
#            "id_cadeira": "22",
#            "id_empresa": "31",
#            "id_mesa": "01",
#            "nome": "Iuri Guilherme"
#          }
#        },
#      ],
#    },
#  ]

def goworking_esqueleto():
  filas = list()
  filas.append(
    {
      'ordem': 0,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 0,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 1,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Jardim",
      'ordem': 2,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Jardim",
      'ordem': 3,
      'id_mesa': None,
    }
  )
  filas.append(
    {
      'ordem': 1,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 4,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 5,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 01",
      'ordem': 6,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 1,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 02",
      'ordem': 7,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 2,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 2,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 8,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Auditório",
      'ordem': 9,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 03",
      'ordem': 10,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 3,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 04",
      'ordem': 11,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 4,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 3,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Corredor",
      'ordem': 12,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Corredor",
      'ordem': 13,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 05",
      'ordem': 14,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 5,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 06",
      'ordem': 15,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 6,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 4,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Banheiro Masculino",
      'ordem': 16,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Chuveiro",
      'ordem': 17,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 07",
      'ordem': 18,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 7,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 08",
      'ordem': 19,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 8,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 5,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Banheiro Feminino",
      'ordem': 20,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Banheiro PCD",
      'ordem': 21,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 09",
      'ordem': 22,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 9,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 10",
      'ordem': 23,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 10,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 6,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Banheiro Feminino",
      'ordem': 24,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Parede Grafitada",
      'ordem': 25,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 11",
      'ordem': 26,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 11,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 12",
      'ordem': 27,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 12,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 7,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 17",
      'ordem': 28,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 17,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 18",
      'ordem': 29,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 18,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 13",
      'ordem': 30,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 13,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 14",
      'ordem': 31,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 14,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 8,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 19",
      'ordem': 32,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 19,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 20",
      'ordem': 33,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 20,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 15",
      'ordem': 34,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 15,
      'cadeiras': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Mesa 16",
      'ordem': 35,
      'id_mesa': custom_uuid.default_uuid,
      'numero': 16,
      'cadeiras': list(),
    }
  )
  filas.append(
    {
      'ordem': 9,
      'colunas': list(),
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Sala de reuniões",
      'ordem': 36,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Sala de reuniões",
      'ordem': 37,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Televisão",
      'ordem': 38,
      'id_mesa': None,
    }
  )
  filas[-1]['colunas'].append(
    {
      'desc': u"Recepção",
      'ordem': 39,
      'id_mesa': None,
    }
  )
  for fila in filas:
    for coluna in fila['colunas']:
      if coluna['id_mesa']:
        coluna['cadeiras'].append(
          {
            'ordem': 0,
            'letra': 'A',
            'id': custom_uuid.default_uuid,
          }
        )
        coluna['cadeiras'].append(
          {
            'ordem': 1,
            'letra': 'B',
            'id': custom_uuid.default_uuid,
          }
        )
        coluna['cadeiras'].append(
          {
            'ordem': 2,
            'letra': 'C',
            'id': custom_uuid.default_uuid,
          }
        )
        coluna['cadeiras'].append(
          {
            'ordem': 3,
            'letra': 'D',
            'id': custom_uuid.default_uuid,
          }
        )
  return filas

