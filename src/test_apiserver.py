"""Casos de prueba para el servidor de APIs."""
import messages
from jsonschema import validate
import requests
import pytest
from user import User

# ***** schemas JSON *****
user_201_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "message": {"type": "string"},
    },
    "required": ["id", "message"]
}

error_4XX_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"]
}

error_5XX_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "error": {"type": "string"},
    },
    "required": ["message", "error"]
}


server = "http://localhost:5000/api"
application_json = "application/json; charset=utf-8"

def user(h):
    return f"{server}/user/{h}"

users = f"{server}/user"

# ***** usuarios de prueba *****
USER_TEST = {'name': 'Test', 'email': 'test@test.com', 'age': 25}
USER_TEST_MODIFIED = {'name': 'Test modified', 'email': 'test@modified.com', 'age': 25}
USER_TEST_INVALID = {'name': 'Test', 'email': 'test', 'age': 25} # email inválido
USER_TEST_INVALID_AGE = {'name': 'Test', 'email': 'test_invalid_age@test.com', 'age': -25} # edad negativa

# ***** unit tests with pytest *****
def test_create_user():
    """Valida la creación de un usuario."""
    response = requests.post(users, json=USER_TEST)
    assert response.status_code == 201
    assert response.json()['message'] == messages.USER_CREATED
    assert response.headers['Content-Type'] == application_json
    validate(instance=response.json(), schema=user_201_schema)

def test_invalid_mimetype():
    """Valida el tipo MIME de la solicitud."""
    response = requests.post(users, USER_TEST, headers={'Content-Type': 'text/plain'})
    assert response.status_code == 400
    validate(instance=response.json(), schema=error_4XX_schema)

def test_invalid_data():
    """Valida datos incompletos."""
    response = requests.post(users, json={'name': 'Test'})
    assert response.status_code == 400
    assert response.json()['message'] == messages.INVALID_DATA
    validate(instance=response.json(), schema=error_4XX_schema)

def test_invalid_email():
    """Valida el formato del correo electrónico."""
    response = requests.post(users, json=USER_TEST_INVALID)
    assert response.status_code == 400
    assert response.json()['message'] == messages.INVALID_EMAIL
    validate(instance=response.json(), schema=error_4XX_schema)

def test_email_already_registered():
    """Valida que el correo electrónico no esté registrado."""
    requests.post(users, json=USER_TEST)
    response = requests.post(users, json=USER_TEST)
    assert response.status_code == 400
    assert response.json()['message'] == messages.ALREADY_CREATED
    validate(instance=response.json(), schema=error_4XX_schema)

def test_invalid_age():
    """Valida que la edad no sea negativa."""
    response = requests.post(users, json=USER_TEST_INVALID_AGE)
    assert response.status_code == 400
    assert response.json()['message'] == messages.INVALID_AGE
    validate(instance=response.json(), schema=error_4XX_schema)

def test_get_users():
    """Valida la obtención de la lista de usuarios."""
    requests.post(users, json=USER_TEST)
    response = requests.get(users)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == application_json
    assert isinstance(response.json(), list)

def test_get_user_by_id():
    """Valida la obtención de un usuario por su ID."""
    requests.post(users, json=USER_TEST)
    response = requests.get(user(1))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == application_json
    assert isinstance(response.json(), dict)

def test_user_not_found():
    """Valida que un usuario no exista."""
    response = requests.get(user(100))
    assert response.status_code == 404
    assert response.json()['message'] == messages.USER_NOT_FOUND
    validate(instance=response.json(), schema=error_4XX_schema)

def test_update_user():
    """Valida la actualización de un usuario."""
    requests.post(users, json=USER_TEST)
    response = requests.put(user(1), json=USER_TEST_MODIFIED)
    assert response.status_code == 200
    assert response.json()['message'] == messages.USER_UPDATED
    assert response.headers['Content-Type'] == application_json
    assert isinstance(response.json(), dict)

def test_update_user_not_found():
    """Valida que un usuario no exista para actualizarlo."""
    response = requests.put(user(100), json=USER_TEST_MODIFIED)
    assert response.status_code == 404
    assert response.json()['message'] == messages.USER_NOT_FOUND
    validate(instance=response.json(), schema=error_4XX_schema)

def test_update_user_invalid_data():
    """Valida que los datos para actualizar un usuario sean inválidos."""
    requests.post(users, json=USER_TEST)
    response = requests.put(user(1), json=USER_TEST_INVALID)
    assert response.status_code == 400
    assert response.json()['message'] == messages.INVALID_EMAIL
    validate(instance=response.json(), schema=error_4XX_schema)

def test_update_user_email_already_registered():
    """Valida que el correo electrónico no esté registrado al actualizar un usuario."""
    requests.post(users, json=USER_TEST)
    response = requests.put(user(1), json=USER_TEST)
    assert response.status_code == 400
    assert response.json()['message'] == messages.ALREADY_CREATED
    validate(instance=response.json(), schema=error_4XX_schema)

def test_update_user_invalid_age():
    """Valida que la edad no sea negativa al actualizar un usuario."""
    requests.post(users, json=USER_TEST)
    response = requests.put(user(1), json=USER_TEST_INVALID_AGE)
    assert response.status_code == 400
    assert response.json()['message'] == messages.INVALID_AGE
    validate(instance=response.json(), schema=error_4XX_schema)

def test_delete_user():
    """Valida la eliminación de un usuario."""
    requests.post(users, json=USER_TEST)
    response = requests.delete(user(1))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == application_json
    assert response.json()['message'] == messages.USER_DELETED

def test_delete_user_not_found():
    """Valida que un usuario no exista para eliminarlo."""
    response = requests.delete(user(100))
    assert response.status_code == 404
    assert response.json()['message'] == messages.USER_NOT_FOUND
    validate(instance=response.json(), schema=error_4XX_schema)

def test_delete_all_users():
    """Valida la eliminación de todos los usuarios."""
    usuarios = requests.get(users).json()
    for usuario in usuarios:
        response = requests.delete(user(usuario['id']))    
        assert response.status_code == 200
        assert response.headers['Content-Type'] == application_json
        assert response.json()['message'] == messages.USER_DELETED

    response = requests.get(users)
    assert response.status_code == 200
    assert response.json() == []