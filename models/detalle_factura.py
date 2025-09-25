from database import db

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)    
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)    
    subtotal = db.Column(db.Numeric(10,2), nullable=False)