# vim:fileencoding=utf-8
## Filtros para Jinja

import babel
import re

def filtro_data(data):
  formato = "dd/MM/YYYY"
  return babel.dates.format_datetime(data, formato)

## TJEMSE - Tudo Junto E Minúsculo Sem Espaços
def filtro_tjemse(string):
  return re.sub(r"\s+", "", string.lower(), flags=re.UNICODE)

