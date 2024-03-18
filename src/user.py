import messages

class User:

    required_fields = ['name', 'email', 'age']

    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    @property  # getter
    def email(self):
        return self._email

    @email.setter # setter
    def email(self, value):
        if '@' not in value:
            raise ValueError(messages.INVALID_EMAIL)
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError(messages.INVALID_AGE)
        self._age = value

    @classmethod
    def validate_fields(cls, data):
        """Valida que los datos contengan los campos requeridos"""
        if not data or not all(field in data for field in cls.required_fields):
            raise ValueError(messages.INVALID_DATA)
        return True