# API de Inventario

La aplicación es una API REST desarrollada con Flask para gestionar productos de un inventario.

## Tecnologías utilizadas

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-Migrate
- JWT
- Bruno
- Render

## Funcionalidades

- Registro de usuarios
- Login
- Autenticación con JWT
- Roles de usuario y administrador
- CRUD completo de productos
- Rutas protegidas
- Base de datos PostgreSQL
- API desplegada en producción

## Endpoints principales

```text
POST   /auth/register
POST   /auth/login

GET    /productos
GET    /productos/<id>
POST   /productos
PUT    /productos/<id>
DELETE /productos/<id>
```

Los usuarios autenticados pueden consultar productos.

Las operaciones de crear, actualizar y eliminar productos están limitadas al rol `admin`.

## Base de datos

Se utiliza PostgreSQL junto con SQLAlchemy como ORM.

Las tablas principales son:

```text
usuarios
productos
```

## Producción

La API se encuentra desplegada en Render:

```text
https://inventario-api-flask.onrender.com
```

Los endpoints fueron probados utilizando Bruno.