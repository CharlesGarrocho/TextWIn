import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, Response
import json


# Configuracoes do Aplicacao Flask
app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(__name__)

# Configuracoes do Banco de Dados
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'chat.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#########################################################
##### INICIO DO BLOCO DAS FUNCOES DO BANCO DE DADOS #####
#########################################################
def bd_conecta():
    """Conecta ao banco de dados especificado."""
    if not hasattr(g, 'sqlite_db'):
        rv = sqlite3.connect(app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        g.sqlite_db = rv
    return g.sqlite_db

@app.teardown_appcontext
def bd_fechar(error):
    """Fecha o Banco de Dados ao Fim da Requisicao."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def bd_iniciar():
    """Inicia a Conexao com o Banco de Dados."""
    db = bd_conecta()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def bd_obter_mensagens():
    db = bd_conecta()
    cur = db.execute('select nome, mensagem from mensagens order by id desc')
    column_names = [d[0] for d in cur.description]
    mensagens = []
    for row in cur:
      info = dict(zip(column_names, row))
      mensagens.append(info)
    return mensagens

def bd_adicionar_mensagem(nome, mensagem):
    db = bd_conecta()
    db.execute('insert into mensagens (nome, mensagem) values (?, ?)',
                 [nome, mensagem])
    db.commit()

###################################################
##### INICIO DO BLOCO DAS FUNCOES DO REST API #####
###################################################
@app.route('/')
def pagina_inicial():
    return "<h1>Bem Vindo ao Chat</h1>Altere o projeto Listas transformando em um Chat.<br><br> <h2>Instrucoes:</h2>Para acessar as mensagens: 192.168.10.102:5000/mensagens <br> <br> Para adicionar uma mensagem: 192.168.10.102:5000/adicionar?nome=SeuNome&mensagem=SuaMensagem <br> <br> <h2>Android</h2> Exemplo de Requisicao a um site: http://stackoverflow.com/questions/3505930/make-an-http-request-with-android <br> <br> Exemplo de Parse no Json: http://stackoverflow.com/questions/18977144/how-to-parse-json-array-not-json-object-in-android"

@app.route('/mensagens')
def listar_mensagens():
    mensagens = bd_obter_mensagens()
    return jsonify(mensagens)

@app.route('/adicionar')
def adiciona_mensagem():
    print request.args
    if 'nome' in request.args and 'mensagem' in request.args:
        bd_adicionar_mensagem(request.args['nome'], request.args['mensagem'])
        return "SIM"
    else:
        return "NAO"


if __name__ == "__main__":
    app.run(host='192.168.10.106')