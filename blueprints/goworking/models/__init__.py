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

## Versão 1
#from blueprints.goworking.models.login import user_v1
#from blueprints.goworking.models.goworking import mesa_v1, cadeira_v1, empresa_v1, habitante_v1

## Versão atual
from blueprints.goworking.models.login import User
from blueprints.goworking.models.goworking import (
  espaco,
  mesa,
  cadeira,
  empresa,
  habitante,
)

