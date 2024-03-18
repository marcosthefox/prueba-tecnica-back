#!/usr/bin/env python3
from flask import Flask, jsonify, request
from typing import Dict
import messages
from user import User

app = Flask(__name__)

"""Almacenamiento en memoria para los datos de usuario:
{
    1: User(id=1, name='Juan', email='...@...', age=25),
    2: User(id=2, name='Pedro', email='...@...', age=30),
    ...
}"""
users_db: Dict[int, 'User'] = {} # se utiliza un diccionario que tiene como clave el id del usuario y como valor el objeto User. La clase User se importa desde user.py


# **** endpoints ****
@app.post("/api/user")
def create_user():
    """Crea un nuevo usuario."""
    if request.mimetype != "application/json":
        return jsonify(message=f"Invalid message mimetype: '{request.mimetype}'"), 400

    data = request.json
    try:
        User.validate_fields(data)
    except ValueError as e:
        return jsonify(message=str(e)), 400

    email = data['email']
    if email in [user.email for user in users_db.values()]:
        return jsonify(message=messages.ALREADY_CREATED), 400

    try:
        user_id = len(users_db) + 1
        new_user = User(user_id, data['name'], data['email'], data['age'])
        users_db[user_id] = new_user
        return jsonify(message=messages.USER_CREATED, id=user_id), 201, {"Content-Type": "application/json; charset=utf-8"}
    except ValueError as e:
        return jsonify(message=str(e)), 400
    except Exception as e:
        return jsonify(message=messages.INTERNAL_ERROR), 500

@app.get("/api/user")
def get_users():
    """Obtiene la lista de usuarios."""
    users_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age} for user in users_db.values()]
    return jsonify(users_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.get("/api/user/<int:user_id>")
def get_user_by_id(user_id):
    """Obtiene un usuario por su ID. Si el usuario no existe, retorna un error 404."""
    user = users_db.get(user_id)
    if user is None:
        return jsonify(message=messages.USER_NOT_FOUND), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.put("/api/user/<int:user_id>")
def user_update(user_id):
    """Actualiza los datos de un usuario. Si el usuario no existe, retorna un error 404. Si los datos son inválidos, retorna un error 400."""
    user = users_db.get(user_id)
    if user is None:
        return jsonify(message=messages.USER_NOT_FOUND), 404

    data = request.json
    try:
        User.validate_fields(data)
    except ValueError as e:
        return jsonify(message=str(e)), 400

    email = data.get('email')
    if email and email != user.email and email in [user.email for user in users_db.values()]:
        return jsonify(message=messages.ALREADY_CREATED), 400

    try:
        user.name = data.get('name', user.name) #si no se especifica, se mantiene el valor actual
        user.email = data.get('email', user.email)
        user.age = data.get('age', user.age)
        return jsonify(message=messages.USER_UPDATED), 200, {"Content-Type": "application/json; charset=utf-8"}
    except ValueError as e:
        return jsonify(message=str(e)), 400
    except Exception as e:
        return jsonify(message=messages.INTERNAL_ERROR), 500
    
@app.delete("/api/user/<int:user_id>")
def user_delete(user_id):
    """Elimina un usuario por su ID. Si el usuario no existe, retorna un error 404."""
    if user_id not in users_db:
        return jsonify(message=messages.USER_NOT_FOUND), 404
    del users_db[user_id]
    return jsonify(message=messages.USER_DELETED), 200, {"Content-Type": "application/json; charset=utf-8"}


if __name__ == '__main__':
    app.run(debug=True)