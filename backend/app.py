# backend/app.py
import os, sqlite3
from flask import jsonify
from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
DB_PATH  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.db'))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='/')

@app.get('/api/eventos')
def api_eventos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, titulo, descripcion, fecha_hora, lugar, aforo, entradas_disponibles
        FROM eventos
        ORDER BY datetime(fecha_hora) ASC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    print(f"🔌 Usando base de datos: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cur = conn.cursor()

    # Usuarios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Eventos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        fecha_hora TEXT NOT NULL,   -- ISO string YYYY-MM-DD HH:MM
        lugar TEXT NOT NULL,
        aforo INTEGER NOT NULL,
        entradas_disponibles INTEGER NOT NULL
    );
    """)

    conn.commit()

    # Semilla de eventos si está vacía
    cur.execute("SELECT COUNT(*) AS c FROM eventos")
    if cur.fetchone()["c"] == 0:
        cur.executemany("""
        INSERT INTO eventos (titulo, descripcion, fecha_hora, lugar, aforo, entradas_disponibles)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("Concierto Rock", "Banda local con repertorio clásico.", "2025-10-10 21:00", "Madrid", 300, 300),
            ("Charla de Tecnología", "Novedades IA y Web.", "2025-10-20 18:30", "Barcelona", 120, 120),
            ("Monólogo", "Noche de comedia.", "2025-11-05 20:00", "Valencia", 200, 200),
        ])
        conn.commit()
        print("🌱 Eventos de ejemplo insertados.")
    conn.close()
    print("✅ Tablas comprobadas/creadas.")

# --- 💡 Llamamos a init_db() al importar el módulo (sin decoradores) ---
init_db()

@app.get('/')
def home():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    print("👉 Petición:", request.method, request.path)
    if request.method == 'GET':
        return send_from_directory(BASE_DIR, 'registro.html')

    nombre    = request.form.get('nombre', '').strip()
    email     = request.form.get('email', '').strip()
    password  = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if not nombre or not email or len(password) < 6 or password != password2:
        return render_template_string('<h1>Datos inválidos</h1><p><a href="/registro">Volver</a></p>'), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
            (nombre, email, generate_password_hash(password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template_string('<h1>Error: el usuario ya existe</h1><p><a href="/registro">Volver</a></p>'), 400
    finally:
        conn.close()

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("👉 Petición:", request.method, request.path)
    if request.method == 'GET':
        return send_from_directory(BASE_DIR, 'login.html')

    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return render_template_string('<h1>Bienvenido {{n}}</h1><p><a href="/">Inicio</a></p>', n=user["nombre"])
    return render_template_string('<h1>Credenciales incorrectas</h1><p><a href="/login">Volver</a></p>'), 400

if __name__ == '__main__':
    app.run(debug=True)
    