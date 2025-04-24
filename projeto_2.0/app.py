from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quem_somos')
def quem_somos():
    return render_template('quem_somos.html')

@app.route('/eventos')
def eventos():
    return render_template('eventos.html')

@app.route('/doacao')
def doacao():
    return render_template('doacao.html')

@app.route('/prestacao_contas')
def contas():
    return render_template('prestacao_contas.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/redes_sociais')
def redes_sociais():
    return render_template('redes_sociais.html')

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/reunioes')
def reunioes():
    return render_template('reunioes.html')

@app.route('/proximos_eventos')
def proximos_eventos():
    return render_template('proximos_eventos.html')