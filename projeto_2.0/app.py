from flask import Flask, render_template
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for
from flask import request, redirect, url_for
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask import flash

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    image_filename = db.Column(db.String(200))

#Modelo de usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Pode ser hash se quiser segurança extra

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#Config. flask login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Em produção, use hash + verificação

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos')

    return render_template('login.html')

#Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



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
    posts = Posts.query.all()
    return render_template('proximos_eventos.html', posts=posts)

@app.route('/contas_doacao')
def contas_doacao():
    return render_template('contas_doacao.html')

@app.route('/deletar_evento/<int:post_id>', methods=['POST'])
@login_required #add requerimento de login
def deletar_evento(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('proximos_eventos'))

# Define onde as imagens serão armazenadas
app.config['UPLOAD_FOLDER'] = 'static/img/uploads'  # Pasta onde as imagens serão salvas
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Função para criar um novo evento
@app.route('/novo_evento', methods=['GET', 'POST'])
@login_required #add requerimento de login
def novo_evento(): 
    if request.method == 'POST':
        print("Formulário enviado")
        title = request.form['title']
        content = request.form['content']
        image = request.files.get('image')  # Recebe a imagem, se houver

        # Salvar a imagem se houver
        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)  # Garantir que o nome do arquivo seja seguro
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))  # Salvar a imagem na pasta definida

        # Criar o novo post
        new_post = Posts(title=title, content=content, image_filename=image_filename)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('proximos_eventos'))

    return render_template('novo_evento.html')