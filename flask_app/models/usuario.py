from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    DB = "esquema_bookhub"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, {'email': email})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, {'id': user_id})
        if not results:
            return None
        return cls(results[0])

    @staticmethod
    def validar_registro(usuario):
        is_valid = True

        if len(usuario['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if len(usuario['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if not EMAIL_REGEX.match(usuario['email']):
            flash("El correo electrónico no es válido.", "registro")
            is_valid = False
        else:
            if Usuario.get_by_email(usuario['email']):
                flash("El correo electrónico ya está registrado.", "registro")
                is_valid = False

        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            is_valid = False

        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid