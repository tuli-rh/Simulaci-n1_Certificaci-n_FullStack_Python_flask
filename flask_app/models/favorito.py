from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.libro import Libro

class Favorito:
    DB = "esquema_bookhub"

    @classmethod
    def add_favorito(cls, data):
        query = "INSERT IGNORE INTO favoritos (usuario_id, libro_id) VALUES (%(usuario_id)s, %(libro_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def es_favorito(cls, data):
        query = "SELECT * FROM favoritos WHERE usuario_id = %(usuario_id)s AND libro_id = %(libro_id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return len(results) > 0

    @classmethod
    def get_usuarios_favorito(cls, libro_id):
        query = """
            SELECT u.nombre
            FROM favoritos f
            JOIN usuarios u ON f.usuario_id = u.id
            WHERE f.libro_id = %(libro_id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'libro_id': libro_id})
        return [row['nombre'] for row in results] if results else []

    @classmethod
    def get_favoritos_por_usuario(cls, usuario_id):
        query = """
            SELECT l.*, f.created_at AS fecha_agregado
            FROM favoritos f
            JOIN libros l ON f.libro_id = l.id
            WHERE f.usuario_id = %(usuario_id)s
            ORDER BY f.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'usuario_id': usuario_id})
        favoritos = []
        if results:
            for row in results:
                libro = Libro(row)
                libro.fecha_favorito = row['fecha_agregado']
                favoritos.append(libro)
        return favoritos