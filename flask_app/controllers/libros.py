from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.libro import Libro
from flask_app.models.favorito import Favorito

@app.route('/libros')
def mis_libros():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario_id = session['usuario_id']
    mis_libros = Libro.get_mis_libros(usuario_id)
    libros_comunidad = Libro.get_libros_comunidad(usuario_id)
    
    # Esto te mostrará en la consola si hay libros recuperados de la DB
    print("MIS LIBROS OBTENIDOS:", len(mis_libros))
    
    return render_template('mis_libros.html', mis_libros=mis_libros, libros_comunidad=libros_comunidad)

@app.route('/libros/nuevo')
def nuevo_libro():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('nuevo_libro.html')

@app.route('/libros/crear', methods=['POST'])
def crear_libro():
    if 'usuario_id' not in session:
        return redirect('/')

    # 1. Imprimir los datos que llegan del formulario
    print("\n--- DATOS RECIBIDOS DEL FORMULARIO ---")
    print(request.form)

    # 2. Verificar la validación
    es_valido = Libro.validar_libro(request.form)
    print("¿PASÓ LA VALIDACIÓN?:", es_valido)

    if not es_valido:
        print("---> Falló la validación, redirigiendo a /libros/nuevo\n")
        return redirect('/libros/nuevo')

    data = {
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'genero': request.form['genero'],
        'fecha_publicacion': request.form['fecha_publicacion'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }
    
    # 3. Intentar guardar y ver el ID generado
    nuevo_id = Libro.save(data)
    print("RESULTADO DE LA INSERCIÓN EN MYSQL (ID/Status):", nuevo_id)
    print("---------------------------------------\n")

    return redirect('/libros')

@app.route('/libros/<int:id>')
def mostrar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    libro = Libro.get_by_id(id)
    if not libro:
        return redirect('/libros')

    es_fav = Favorito.es_favorito({'usuario_id': session['usuario_id'], 'libro_id': id})
    usuarios_fav = Favorito.get_usuarios_favorito(id)

    return render_template('detalle_libro.html', libro=libro, es_favorito=es_fav, usuarios_fav=usuarios_fav)

@app.route('/libros/editar/<int:id>')
def editar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    libro = Libro.get_by_id(id)
    if not libro or libro.usuario_id != session['usuario_id']:
        return redirect('/libros')

    return render_template('editar_libro.html', libro=libro)

@app.route('/libros/actualizar/<int:id>', methods=['POST'])
def actualizar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    libro = Libro.get_by_id(id)
    if not libro or libro.usuario_id != session['usuario_id']:
        return redirect('/libros')

    if not Libro.validar_libro(request.form):
        return redirect(f'/libros/editar/{id}')

    data = {
        'id': id,
        'titulo': request.form['titulo'],
        'autor': request.form['autor'],
        'genero': request.form['genero'],
        'fecha_publicacion': request.form['fecha_publicacion'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }
    Libro.update(data)
    return redirect('/libros')

@app.route('/libros/borrar/<int:id>')
def borrar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'id': id,
        'usuario_id': session['usuario_id']
    }
    Libro.delete(data)
    return redirect('/libros')

@app.route('/favoritos/agregar/<int:libro_id>')
def agregar_favorito(libro_id):
    if 'usuario_id' not in session:
        return redirect('/')

    Favorito.add_favorito({'usuario_id': session['usuario_id'], 'libro_id': libro_id})
    return redirect(f'/libros/{libro_id}')

@app.route('/favoritos')
def mis_favoritos():
    if 'usuario_id' not in session:
        return redirect('/')

    favoritos = Favorito.get_favoritos_por_usuario(session['usuario_id'])
    return render_template('mis_favoritos.html', favoritos=favoritos)