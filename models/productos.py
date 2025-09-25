from database import db

class Productos(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(250), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    detalles = db.relationship('DetalleFactura', backref='producto', lazy=True)
    
# def __repr__(self):
#     return f'<User {self.username}>'  