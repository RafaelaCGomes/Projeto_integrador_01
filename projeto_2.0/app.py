from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
import datetime

# Configuração do app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'database.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_file


# Definindo as extensões permitidas
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Configuração da pasta de upload
app.config['UPLOAD_FOLDER_EVENTOS'] = os.path.join('static', 'img', 'uploads')  # Pasta para eventos
app.config['UPLOAD_FOLDER_GALERIA'] = os.path.join('static', 'img', 'galeria')  # Pasta para galeria
app.config['UPLOAD_FOLDER_CONTAS'] = os.path.join('static', 'img', 'prest_contas')  # Pasta para prestação de contas


# Função utilitária para verificar extensões de arquivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Inicializando o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Postagem
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    image_filename = db.Column(db.String(200))

# Tabela Galeria
class Galeria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    image_filenames = db.Column(db.String(5000))  # Agora será uma string com os nomes das imagens separados por ';'

#Tabela Prestação de contas
class prestacaocontas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    image_filenames = db.Column(db.String(5000))

# Modelo de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Função para criar as tabelas no banco de dados
with app.app_context():
    db.create_all()  # Isso cria todas as tabelas definidas no seu código, incluindo posts e galeria.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas públicas
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
    posts = prestacaocontas.query.all()
    return render_template('prestacao_contas.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/redes_sociais')
def redes_sociais():
    return render_template('redes_sociais.html')

@app.route('/reunioes')
def reunioes():
    return render_template('reunioes.html')

@app.route('/contas_doacao')
def contas_doacao():
    return render_template('contas_doacao.html')

@app.route('/galeria')
def galeria():
    # Aqui estamos buscando as postagens da tabela Galeria
    posts = Galeria.query.all()
    return render_template('galeria.html', posts=posts)

# Login / Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Criar novo evento
@app.route('/novo_evento', methods=['GET', 'POST'])
@login_required
def novo_evento():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files.get('image')

        image_filename = None
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER_EVENTOS'], image_filename))

        new_post = Posts(title=title, content=content, image_filename=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('proximos_eventos'))

    return render_template('novo_evento.html')

# Página com próximos eventos
@app.route('/proximos_eventos')
def proximos_eventos():
    posts = Posts.query.order_by(Posts.created.desc()).all()
    return render_template('proximos_eventos.html', posts=posts)

# Deletar evento
@app.route('/deletar_evento/<int:post_id>', methods=['POST'])
@login_required
def deletar_evento(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('proximos_eventos'))

@app.route('/novo_galeria', methods=['GET', 'POST'])
@login_required
def novo_galeria():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        images = request.files.getlist('images')  # Usando getlist para pegar múltiplos arquivos

        image_filenames = []  # Lista para armazenar os nomes das imagens
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)  # Garantir nome seguro
                upload_path = os.path.join(app.config['UPLOAD_FOLDER_GALERIA'], filename)
                print(f"Salvando imagem em: {upload_path}")  # Agora funciona corretamente
                image.save(upload_path)
                image_filenames.append(filename)

            # if image and allowed_file(image.filename):
            #     filename = secure_filename(image.filename)  # Garantir o nome seguro
            #     image.save(os.path.join(app.config['UPLOAD_FOLDER_GALERIA'], filename))
            #     print(f"Salvando imagem em: {upload_path}") 
            #     image_filenames.append(filename)  # Adiciona o nome da imagem à lista

        # Salvando os nomes das imagens como uma única string separada por ponto e vírgula
        new_post = Galeria(
            title=title, 
            content=content, 
            image_filenames=";".join(image_filenames)  # Salva as imagens concatenadas por ponto e vírgula
        )  
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('galeria'))

    return render_template('novo_galeria.html')


# Deletar imagem da galeria
@app.route('/deletar_galeria/<int:post_id>', methods=['POST'])
@login_required
def deletar_galeria(post_id):
    post = Galeria.query.get_or_404(post_id)  # Buscar na tabela Galeria
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('galeria'))

@app.route('/novo_contas', methods=['GET', 'POST'])
@login_required
def novo_contas():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        images = request.files.getlist('images')  # Usando getlist para pegar múltiplos arquivos

        image_filenames = []  # Lista para armazenar os nomes das imagens
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)  # Garantir nome seguro
                upload_path = os.path.join(app.config['UPLOAD_FOLDER_CONTAS'], filename)
                print(f"Salvando imagem em: {upload_path}")  # Agora funciona corretamente
                image.save(upload_path)
                image_filenames.append(filename)

        # Salvando os nomes das imagens como uma única string separada por ponto e vírgula
        new_post = prestacaocontas(
            title=title, 
            content=content, 
            image_filenames=";".join(image_filenames)  # Salva as imagens concatenadas por ponto e vírgula
        )  
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('contas'))

    return render_template('novo_contas.html')

# Deletar imagem de contas
@app.route('/deletar_contas/<int:post_id>', methods=['POST'])
@login_required
def deletar_contas(post_id):
    post = prestacaocontas.query.get_or_404(post_id)  # Buscar na tabela Galeria
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('contas'))

