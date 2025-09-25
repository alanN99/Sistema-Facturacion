from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # guardás el hash
    rol = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        """Genera y guarda el hash de la contraseña"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        return check_password_hash(self.password, password)