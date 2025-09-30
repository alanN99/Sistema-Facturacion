from database import db

class Clientes(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)    
    direccion = db.Column(db.String(250), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)