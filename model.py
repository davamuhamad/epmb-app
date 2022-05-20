
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# MODEL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://xqvpshktlurrof:fb94b9298abcf47d7f83b1b31f832406aa416dc887487e9ae71a043f1d9d17e4@ec2-54-172-175-251.compute-1.amazonaws.com/db779ushpgr5k4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer,primary_key=True)
    username = db. Column(db.String(100), nullable = False)
    passw = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<User %r>" % self.username

class Info(db.Model):
    __tablename__ = 'info'
    id_info = db.Column(db.Integer,primary_key=True)
    judul = db. Column(db.String, nullable = False)
    deskripsi = db.Column(db.String, nullable = False)

class Pembayar(db.Model):
    __tablename__ = 'pembayar'
    id_bayar = db.Column(db.Integer,primary_key=True)
    id_user = db.Column(db.Integer, nullable = False)
    tgl_bayar = db.Column(db.Date, nullable = False)
    status_bayar = db.Column(db.String, nullable = False)
    bukti_tf = db.Column(db.LargeBinary, nullable = False)