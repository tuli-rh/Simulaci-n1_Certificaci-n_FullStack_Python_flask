from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/libros')
    return render_template('login_registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = Usuario.save(data)
    session['usuario_id'] = user_id
    session['usuario_nombre'] = request.form['nombre']
    return redirect('/libros')

@app.route('/login', methods=['POST'])
def login():
    user = Usuario.get_by_email(request.form['email'])
    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Credenciales inválidas.", "login")
        return redirect('/')

    session['usuario_id'] = user.id
    session['usuario_nombre'] = user.nombre
    return redirect('/libros')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')