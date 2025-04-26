from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear la base de datos y tablas si no existen
def crear_base():
    conn = sqlite3.connect("merak.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        tipo TEXT,
        esencia TEXT,
        tematica TEXT,
        precio REAL,
        contenido_digital BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total REAL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER,
        precio_unitario REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    """)

    conn.commit()
    conn.close()

# Llamar función al iniciar
crear_base()

# Rutas básicas (puedes expandirlas luego)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]

        conn = sqlite3.connect("merak.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, correo, direccion, telefono) 
            VALUES (?, ?, ?, ?) 
        """, (nombre, correo, direccion, telefono))
        conn.commit()
        conn.close()
        return redirect("/clientes")
    return render_template("formulario_cliente.html")  # formulario para registrar clientes

@app.route("/clientes")
def clientes():
    conn = sqlite3.connect("merak.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("lista_clientes.html", clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
