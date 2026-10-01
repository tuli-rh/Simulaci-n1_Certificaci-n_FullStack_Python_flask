from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date

class Libro:
    DB = "esquema_bookhub"

    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.autor = data['autor']
        self.genero = data['genero']
        self.fecha_publicacion = data['fecha_publicacion']
        self.descripcion = data['descripcion']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creador_nombre = data.get('creador_nombre', '')
        self.total_favoritos = data.get('total_favoritos', 0)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO libros (titulo, autor, genero, fecha_publicacion, descripcion, usuario_id) VALUES (%(titulo)s, %(autor)s, %(genero)s, %(fecha_publicacion)s, %(descripcion)s, %(usuario_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_mis_libros(cls, usuario_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre,
                COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id = %(usuario_id)s
            GROUP BY l.id
            ORDER BY l.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'usuario_id': usuario_id})
        libros = []
        if results and isinstance(results, list):
            for row in results:
                libros.append(cls(row))
        return libros

    @classmethod
    def get_libros_comunidad(cls, usuario_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre,
                COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id != %(usuario_id)s
            GROUP BY l.id
            ORDER BY l.created_at DESC;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'usuario_id': usuario_id})
        libros = []
        if results and isinstance(results, list):
            for row in results:
                libros.append(cls(row))
        return libros
    
    @classmethod
    def get_by_id(cls, libro_id):
        query = """
            SELECT l.*, u.nombre AS creador_nombre
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            WHERE l.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, {'id': libro_id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE libros 
            SET titulo = %(titulo)s, autor = %(autor)s, genero = %(genero)s, 
                fecha_publicacion = %(fecha_publicacion)s, descripcion = %(descripcion)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM libros WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validar_libro(libro):
        is_valid = True

        if len(libro.get('titulo', '').strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "libro")
            is_valid = False

        if len(libro.get('autor', '').strip()) < 2:
            flash("El nombre del autor debe tener al menos 2 caracteres.", "libro")
            is_valid = False

        if not libro.get('genero') or libro.get('genero') == "":
            flash("Debe seleccionar un género.", "libro")
            is_valid = False

        if not libro.get('fecha_publicacion'):
            flash("Debe ingresar una fecha de publicación.", "libro")
            is_valid = False
        else:
            try:
                fecha_ingresada = datetime.strptime(libro['fecha_publicacion'], "%Y-%m-%d").date()
                if fecha_ingresada > date.today():
                    flash("La fecha de publicación no puede ser una fecha futura.", "libro")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha no válido.", "libro")
                is_valid = False

        if len(libro.get('descripcion', '').strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "libro")
            is_valid = False

        return is_valid

    @classmethod
    def agregar_favorito(cls, data):
        query = "INSERT INTO favoritos (usuario_id, libro_id) VALUES (%(usuario_id)s, %(libro_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)