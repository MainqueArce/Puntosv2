from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear tabla si no existe
def init_db():
    with sqlite3.connect("clientes.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                puntos INTEGER DEFAULT 0
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        with sqlite3.connect("clientes.db") as conn:
            try:
                conn.execute("INSERT INTO clientes (nombre) VALUES (?)", (nombre,))
                conn.commit()
                return redirect('/')
            except:
                return "Cliente ya registrado."
    return render_template('registrar.html')

@app.route('/sumar', methods=['POST'])
def sumar():
    nombre = request.form['nombre']
    puntos = int(request.form['puntos'])
    with sqlite3.connect("clientes.db") as conn:
        conn.execute("UPDATE clientes SET puntos = puntos + ? WHERE nombre = ?", (puntos, nombre))
        conn.commit()
    return redirect('/')

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    puntos = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        with sqlite3.connect("clientes.db") as conn:
            cursor = conn.execute("SELECT puntos FROM clientes WHERE nombre = ?", (nombre,))
            fila = cursor.fetchone()
            puntos = fila[0] if fila else "No encontrado"
    return render_template('consultar.html', puntos=puntos)

@app.route('/canjear', methods=['GET', 'POST'])
def canjear():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form['nombre']
        puntos = int(request.form['puntos'])
        with sqlite3.connect("clientes.db") as conn:
            cursor = conn.execute("SELECT puntos FROM clientes WHERE nombre = ?", (nombre,))
            fila = cursor.fetchone()
            if fila and fila[0] >= puntos:
                conn.execute("UPDATE clientes SET puntos = puntos - ? WHERE nombre = ?", (puntos, nombre))
                conn.commit()
                mensaje = "Canje exitoso"
            else:
                mensaje = "No tiene suficientes puntos o no existe"
    return render_template('canjear.html', mensaje=mensaje)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
