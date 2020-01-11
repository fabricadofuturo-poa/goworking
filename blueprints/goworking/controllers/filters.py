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
## Filtros para Jinja

import babel
import re

def filtro_data(data):
  formato = "dd/MM/YYYY"
  return babel.dates.format_datetime(data, formato)

## TJEMSE - Tudo Junto E Minúsculo Sem Espaços
def filtro_tjemse(string):
  return re.sub(r"\s+", "", string.lower(), flags=re.UNICODE)

def filtro_dezena(numero):
  return "{:02d}".format(numero)

def filtro_cpf(cpf):
  cpf = str(cpf)
  if len(cpf) == 11:
    return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
  return cpf

def filtro_cnpj(cnpj):
  cpnj = str(cnpj)
  if len(cnpj) == 14:
    return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
  return cpnj
