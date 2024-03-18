# Backend 

## Descripción

Este repositorio contiene un script de Python que maneja las solicitudes HTTP a un servidor.
Este script depende de la biblioteca Flask para manejar las solicitudes y respuestas HTTP.
Fue creado para Global Think Technology.


## Build
```python
python3 apiserver.py
```
El archivo `apiserver` se encuentra en el directorio `src`.

La url por default es la siguiente: http://localhost:5000/api

## Requerimientos de ejecucion
Los requerimientos para ejecutar el proyecto se encuentran en el archivo [requirements](./requirements.txt).

Usted los puede instalar con el siguiente comando
```python
pip install -r requirements.txt
```

## Endpoints Adicionales

### `POST /user`

Crea un nuevo usuario.

- **Request body:**
```python
{
    "name": "string",
    "email": "...@...",
    "age": "integer"
}
```

- **Responses:**
  * Código HTTP: 201
  * Cuerpo:
    * "message": `USER_CREATED`.
    * "id": id asignado al usuario.
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_MIMETYPE`. 
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_DATA`.
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_EMAIL`. 
  * Código HTTP: 400
  * Cuerpo:
    * "message": `ALREADY_CREATED`.
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_AGE`. 
  * Código HTTP: 500
  * Cuerpo:
    * "message": `INTERNAL_ERROR`.

### `GET /user`

Obtiene la lista de usuarios.

- **Parameters:**
No content.

- **Responses:**
  * Código HTTP: 200
  * Cuerpo:
    * El objeto usuario.
    * si no hay usuarios cargados, se muestra una lista vacía.

### `GET /user/{user_id}`

Obtiene un usuario por su ID.

- **Parameters:**
  * Nombre:
    * user_id.
  * Descripcion:
    * Id del usuario a obtener. Es un campo de tipo `integer`.

- **Responses:**
  * Código HTTP: 200
  * Cuerpo:
    * el objeto usuario.
  * Código HTTP: 404
  * Cuerpo:
    * "message": `USER_NOT_FOUND`.

### `PUT /user/{user_id}`

Actualiza un usuario por su ID.

- **Parameters:**
  * Nombre:
    * user_id.
  * Descripcion:
    * Id del usuario. Es un campo de tipo `integer`.

- **Request body:**
```python
{
    "name": "string",
    "email": "...@...",
    "age": "integer"
}
```

- **Responses:**
  * Código HTTP: 200
  * Cuerpo:
    * "message": `USER_UPDATED`.
  * Código HTTP: 404
  * Cuerpo:
    * "message": `USER_NOT_FOUND`. 
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_DATA`.
  * Código HTTP: 400
  * Cuerpo:
    * "message": `ALREADY_CREATED`. 
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_EMAIL`. 
  * Código HTTP: 400
  * Cuerpo:
    * "message": `INVALID_AGE`. 
  * Código HTTP: 500
  * Cuerpo:
    * "message": `INTERNAL_ERROR`.

### `DELETE /user/{user_id}`

Elimina un usuario por su ID.

- **Parameters:**
  * Nombre:
    * user_id.
  * Descripcion:
    * Id del usuario. Es un campo de tipo `integer`.

- **Responses:**
  * Código HTTP: 200
  * Cuerpo:
    * "message": `USER_DELETED`.
  * Código HTTP: 404
  * Cuerpo:
    * "message": `USER_NOT_FOUND`.


## Mensajes de error

- **INVALID_DATA:** "Datos incompletos"
- **INVALID_MIMETYPE:** "Tipo MIME inválido"
- **INVALID_EMAIL:** "Formato de correo electrónico inválido"
- **ALREADY_CREATED:** "Correo electrónico ya registrado" 
- **INVALID_AGE:** "La edad no puede ser negativa"
- **INTERNAL_ERROR:** "Error interno"
- **USER_CREATED:** "Usuario creado exitosamente"
- **USER_UPDATED:** "Usuario actualizado exitosamente"
- **USER_DELETED:** "Usuario eliminado exitosamente"

## Casos de prueba

Las pruebas unitarias fueron escritas sobre el framework Pytest de Python.
Para ejecutar los test:
```python
pytest test_apiserver.py
```

## cURL básicos para pruebas

### `POST /user`
```bash
curl --location --request POST 'http://localhost:5000/api/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "marcos",
    "email": "marcos@gmail.com",
    "age": 24
}'
```

### `GET /user`
```bash
curl --location --request GET 'http://localhost:5000/api/user'
```

### `GET /user/{user_id}`
```bash
curl --location --request GET 'http://localhost:5000/api/user/1'
```

### `PUT /user/{user_id}`
```bash
curl --location --request PUT 'http://localhost:5000/api/user/1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "ana",
    "email": "ana@gmail.com",
    "age": 22
}'
```

### `DELETE /user/{user_id}`
```bash
curl --location --request DELETE 'http://localhost:5000/api/user/1'
```