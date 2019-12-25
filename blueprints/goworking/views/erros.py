# vim:fileencoding=utf-8
## Erros

from blueprints.goworking import bp
from app import db
from flask import render_template

import werkzeug.exceptions

@bp.errorhandler(werkzeug.exceptions.HTTPException)
def erro(erro):
  return render_template(
    'erro.html',
    title = u"Erro %s" % (erro.code),
    erro = erro,
    mensagem = u"Um problema aconteceu e estamos tentando identificar \
      a causa. Mentira. Na verdade, não tem como saber que o problema \
      aconteceu; nem o motivo, causa, razão ou circunstância; tampouco \
      seremos notificada(o)s acerca deste problema. Se não for pedir \
      muito, por obséquio mui respeitosamente solicitamos à vossa \
      excelência que faça o favor de levantardes da cadeira e nos \
      avise para que pelo menos estejamos cientes de que as coisas não \
      estão funcionando conforme o esperado. Muito obrigado, vós sois \
      muito gentil! \
      TL;DR: Foi mal :/",
  ), erro.code

@bp.errorhandler(404)
def erro_404(erro):
  return render_template(
    'erro.html',
    title = u"Erro %s" % (erro.code),
    erro = erro,
    mensagem = u"Ninguém por aqui ouviu falar desta página. Tem \
      certeza que ela existe?",
  ), erro.code

@bp.errorhandler(500)
def erro_500(erro):
  db.session.rollback()
  return render_template(
    'erro.html',
    title = u"Erro %s" % (erro.code),
    erro = erro,
    mensagem = u"Erro interno do servidor. Alguém fez alguma coisa \
      errada em alguma situação, e as circunstâncias convergiram para \
      este momento, esta página e esta mensagem.",
  ), erro.code

@bp.errorhandler(502)
def erro_502(erro):
  return render_template(
    'erro.html',
    title = u"Erro %s" % (erro.code),
    erro = erro,
    mensagem = u"O Unicórnio Verde saiu do ar. Alguém precisa avisar \
      a pessoa (ir)responsável pelo Backend.",
  ), erro.code

