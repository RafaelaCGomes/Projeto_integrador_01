from flask import Flask, render_template
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy #para leitura dos objs em modelo relacional
import datetime as dt

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

if __name__ == '__main__':
    app.run(debug=True)