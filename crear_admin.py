from getpass import getpass

from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models import Usuario


with app.app_context():
    email = input("Email del administrador: ")
    nombre = input("Nombre del administrador: ")
    password = getpass("Contraseña del administrador: ")

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        print("Ya existe un usuario con ese email.")
    else:
        admin = Usuario(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password),
            rol="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Administrador creado correctamente.")