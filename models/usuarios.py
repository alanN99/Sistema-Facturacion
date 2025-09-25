from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100), nullable=False)    
    rol = db.Column(db.Integer, nullable=False)

# def __repr__(self):
#     return f'<User {self.username}>'

def set_password(password):
    hashed_password = generate_password_hash(password)

def check_password(password, hashed_password):
    check_password_hash(hashed_password, password)    