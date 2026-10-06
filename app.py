from flask import Flask, request
from sqlalchemy import text

from extensions import db, migrate, jwt
from models import Producto, Usuario

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

def es_admin():
    claims = get_jwt()
    return claims.get("rol") == "admin"

@app.route("/")
def inicio():
    return {"mensaje": "API de inventario funcionando"}


@app.route("/db-test")
def db_test():
    db.session.execute(text("SELECT 1"))
    return {"mensaje": "Conexion con PostgreSQL correcta"}

@app.route("/productos", methods=["POST"])
@jwt_required()
def crear_producto():
    if not es_admin():
        return {"error": "Solo administradores pueden crear productos"}, 403

    data = request.get_json()

    if not data or not data.get("nombre") or data.get("precio") is None:
        return {"error": "Nombre y precio son obligatorios"}, 400

    producto = Producto(
        nombre=data["nombre"],
        descripcion=data.get("descripcion"),
        precio=data["precio"],
        stock=data.get("stock", 0)
    )

    db.session.add(producto)
    db.session.commit()

    return {
        "mensaje": "Producto creado correctamente",
        "producto": producto.to_dict()
    }, 201

@app.route("/productos", methods=["GET"])
@jwt_required()
def listar_productos():
    productos = Producto.query.all()

    return {
        "productos": [producto.to_dict() for producto in productos]
    }, 200

@app.route("/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    producto = db.session.get(Producto, id)

    if producto is None:
        return {"error": "Producto no encontrado"}, 404

    return producto.to_dict(), 200

@app.route("/productos/<int:id>", methods=["PUT"])
@jwt_required()
def actualizar_producto(id):
    if not es_admin():
        return {"error": "Solo administradores pueden actualizar productos"}, 403

    producto = db.session.get(Producto, id)

    if producto is None:
        return {"error": "Producto no encontrado"}, 404

    data = request.get_json()

    producto.nombre = data.get("nombre", producto.nombre)
    producto.descripcion = data.get("descripcion", producto.descripcion)
    producto.precio = data.get("precio", producto.precio)
    producto.stock = data.get("stock", producto.stock)

    db.session.commit()

    return {
        "mensaje": "Producto actualizado correctamente",
        "producto": producto.to_dict()
    }, 200

@app.route("/productos/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_producto(id):
    if not es_admin():
        return {"error": "Solo administradores pueden eliminar productos"}, 403

    producto = db.session.get(Producto, id)

    if producto is None:
        return {"error": "Producto no encontrado"}, 404

    db.session.delete(producto)
    db.session.commit()

    return {
        "mensaje": "Producto eliminado correctamente"
    }, 200

@app.route("/auth/register", methods=["POST"])
def registrar_usuario():
    data = request.get_json()

    if not data or not data.get("nombre") or not data.get("email") or not data.get("password"):
        return {"error": "Nombre, email y password son obligatorios"}, 400

    usuario_existente = Usuario.query.filter_by(email=data["email"]).first()

    if usuario_existente:
        return {"error": "El email ya está registrado"}, 409

    password_hash = generate_password_hash(data["password"])

    usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        password=password_hash,
        rol="usuario"
    )

    db.session.add(usuario)
    db.session.commit()

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol
        }
    }, 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return {"error": "Email y password son obligatorios"}, 400

    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if usuario is None or not check_password_hash(
        usuario.password,
        data["password"]
    ):
        return {"error": "Credenciales incorrectas"}, 401

    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"rol": usuario.rol}
    )

    return {
        "mensaje": "Login correcto",
        "access_token": token
    }, 200

if __name__ == "__main__":
    app.run(debug=True)