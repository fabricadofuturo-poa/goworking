# vim:fileencoding=utf-8
## Erros

from blueprints.goworking import bp
from app import db
from flask import render_template

import werkzeug.exceptions

@bp.errorhandler(werkzeug.exceptions.HTTPException)
def erro(erro):
  return render_template('erro.html', title=u"Erro %s" % (erro.code), erro=erro, mensagem=u"Um problema aconteceu e estamos tentando identificar a causa. Mentira. Na verdade, a gente nem vai ficar sabendo que deu um problema, tem que levantar da cadeira aí e ir nos avisar. Foi mal."), erro.code

@bp.errorhandler(404)
def erro_404(erro):
  return render_template('erro.html', title=u"Erro %s" % (erro.code), erro=erro, mensagem=u"Ninguém por aqui ouviu falar desta página. Tem certeza que ela existe?"), erro.code

@bp.errorhandler(500)
def erro_500(erro):
  db.session.rollback()
  return render_template('erro.html', title=u"Erro %s" % (erro.code), erro=erro, mensagem=u"Erro interno do servidor. Alguém fez alguma cacaca no banco de dados."), erro.code

@bp.errorhandler(502)
def erro_502(erro):
  return render_template('erro.html', title=u"Erro %s" % (erro.code), erro=erro, mensagem=u"O Unicórnio Verde saiu do ar. Alguém avisa o (ir)responsável pelo Backend."), erro.code

