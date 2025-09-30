from database import db

class Facturas(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False) 
    fecha = db.Column(db.Date, nullable=False)    
    total = db.Column(db.Numeric(10,2), nullable=False)
    
    detalles = db.relationship('DetalleFactura', backref='factura', lazy=True)
    
    
