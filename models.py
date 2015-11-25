from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1200), unique=True)
    title = db.Column(db.String(1200), unique=True)


    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()
u = User("John", "john@appleseed.com")
db.session.add(u)
db.session.commit()
u2 = User.query.all()
print(u2)
