from flask import Flask, render_template, request, url_for, flash, redirect
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy #para leitura dos objs em modelo relacional
import datetime as dt
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    posts = Posts.query.all()
    return render_template('index.html', posts=posts)

def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post    

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('O ttitulo é obrigatótio')
        else:
            post = Posts(title=title, content=content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')   

if __name__ == '__main__':
    app.run(debug=True)