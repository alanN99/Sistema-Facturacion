from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import date
from models.usuarios import db, Usuarios
from models.productos import db, Productos
from models.clientes import db, Clientes
from models.facturas import db, Facturas
from models.detalle_factura import db, DetalleFactura

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "clave_secreta"
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# INICIO SESION

@app.route("/")
def home():
    return redirect(url_for("login"))

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión", "danger")
            return redirect(url_for("login"))
        if session.get("rol") != 1:
            flash("No tienes permisos de administrador", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        user = Usuarios.query.filter_by(username=username,
        password=password).first()        
    
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["rol"] = user.rol   # 1=Admin, 2=Usuario
            flash("Login exitoso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return redirect(url_for("login"))        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for("login"))

# USUARIOS
@app.route("/agregar/usuario", methods=["GET", "POST"])
def agregar_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        rol = int(request.form["rol"])
        user = Usuarios(username=username, password=password, rol=rol)
        
        if user == Usuarios.query.filter_by(username=user.username):
            flash("El usuario ya existe", "warning")
            return redirect(url_for("agregar_usuario"))
        
        db.session.add(user)
        db.session.commit()
        
        flash("Registro exitoso!", "success")
        return redirect(url_for('login'))
    return render_template("gestor_usuarios.html")

@app.route("/usuarios/")
@login_required
@admin_required
def listaUsuarios():
    usuarios = Usuarios.query.all()
    return render_template("usuarios.html", usuarios = usuarios)
        
@app.route("/eliminar/usuario/<int:id>")
def eliminar_usuario(id):
    user = Usuarios.query.get(id)
        
    if session.get("user_id") == user.id:
        flash("No se puede borrar el usuario logeado", "warning")
        return redirect(url_for("listaUsuarios"))
    
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("listaUsuarios"))

# PRODUCTOS
@app.route("/productos")
@login_required
@admin_required
def listaProductos():
    productos = Productos.query.all()
    return render_template("productos.html", productos = productos)

@app.route("/agregar/producto", methods=["POST", "GET"])
def agregar_producto():
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        
        nuevo = Productos(
                descripcion=descripcion, 
                precio=precio,
                stock=stock
            )
        db.session.add(nuevo)
        db.session.commit()
        
        return redirect(url_for("listaProductos"))
    
    productos = Productos.query.all()
    return render_template("gestor_productos.html", productos = productos)

@app.route("/editar/producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    producto = Productos.query.get_or_404(id)
    if request.method == "POST":
        producto.descripcion = request.form["descripcion"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        
        db.session.commit()
        flash("Producto actualizado", "success")
        return redirect(url_for("listaProductos"))
    
    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar/producto/<int:id>")
def eliminar_producto(id):
    producto = Productos.query.get(id)
    
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("listaProductos"))

# CLIENTES
@app.route("/agregar/cliente", methods=["POST", "GET"])
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]        
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        
        cliente = Clientes(
                nombre=nombre, 
                direccion=direccion,
                telefono=telefono,
                email=email
            )
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente creado", "success")
        return redirect(url_for('listaClientes'))
    
    clientes = Clientes.query.all()
    return render_template("gestor_clientes.html", clientes= clientes)

@app.route("/clientes", methods=["GET"])
@login_required
@admin_required
def listaClientes():
    clientes = Clientes.query.all()
    return render_template("clientes.html", clientes = clientes)

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = Clientes.query.get_or_404(id)
    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.direccion = request.form["direccion"]
        cliente.telefono = request.form["telefono"]
        cliente.email = request.form["email"]
        
        db.session.commit()
        flash("Cliente actualizado", "success")
        return redirect(url_for("listaClientes"))
    
    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/clientes/eliminar/<int:id>")
def eliminar_cliente(id):
    cliente = Clientes.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado", "success")
    return redirect(url_for("dashboard"))

# FACTURAS
@app.route("/agregar/factura", methods=["GET", "POST"])
def nueva_factura():
    if request.method == "POST":
        id_cliente = request.form["id_cliente"]

        factura = Facturas(
            id_cliente=id_cliente,
            fecha=date.today(),
            total=0
        )
        db.session.add(factura)
        db.session.commit()

        return redirect(url_for("agregar_productos", id_factura=factura.id))

    clientes = Clientes.query.all()
    return render_template("gestor_facturas.html", clientes=clientes)

@app.route("/factura/<int:id_factura>/agregar", methods=["GET", "POST"])
def agregar_productos(id_factura):
    factura = Facturas.query.get(id_factura)
    productos = Productos.query.all()

    if request.method == "POST":
        seleccionados = request.form.getlist("producto_id")
        total_factura = 0

        if not seleccionados:
            flash("Debes seleccionar al menos un producto")
            return redirect(url_for("agregar_productos", id_factura=factura.id))

        for pid in seleccionados:
            producto = Productos.query.get(pid)
            cantidad = int(request.form.get(f"cantidad_{pid}", 1))

            if cantidad > producto.stock:
                flash(f"Stock insuficiente para {producto.descripcion}", "error")
                return redirect(url_for("agregar_productos", id_factura=factura.id))

            subtotal = cantidad * producto.precio
            detalle = DetalleFactura(
                id_factura=factura.id,
                id_producto=producto.id,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal
            )
            db.session.add(detalle)

            producto.stock -= cantidad
            total_factura += subtotal

        factura.total = total_factura
        db.session.commit()

        flash("Factura generada correctamente", "success")
        return redirect(url_for("listaFacturas"))

    return render_template("agregar_productos.html", factura=factura, productos=productos)

@app.route("/facturas", methods=["GET"])
def listaFacturas():
    facturas = Facturas.query.all()
    return render_template("facturas.html", facturas = facturas)

@app.route('/consultar/factura/<int:id>', methods=["GET"])
def consultar_factura(id):
    factura = Facturas.query.get(id)
    detalleFactura = DetalleFactura.query.filter_by(id_factura=factura.id).all()
    return render_template('detalle_factura.html', detalleFactura=detalleFactura)

@app.route("/eliminar/factura/int:<id>")
def eliminar_factura(id):
    factura = Facturas.query.get(id)
    db.session.delete(factura)
    db.session.commit()
    flash("Factura eliminada", "success")
    return redirect(url_for("listaFacturas"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
