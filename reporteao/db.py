import sqlite3

db = sqlite3.connect("database.db")

# Inicializa la base de datos
def init():
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reportes(autor, titulo, facultad, descripcion, imagenes, fecha, likes, estado)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(nombre, email, clave, nivel)")
    cursor.execute("CREATE TABLE IF NOT EXISTS codigos(email, codigo, tipo)")

def agregar_reporte(autor, titulo, facultad, descripcion, imagenes):
    cursor = db.cursor()
    cursor.execute("INSERT INTO reportes VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (autor, titulo, facultad, descripcion, imagenes, 0, 0))

def eliminar_reporte(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM reportes WHERE id = ?", (id,))

def actualizar_reporte(id, estado):
    cursor = db.cursor()
    cursor.execute("UPDATE reportes SET estado = ? WHERE id = ?", (estado, id))

def listar_reportes(ubicacion):
    cursor = db.cursor()
    fin = ubicacion + 20
    res = cursor.execute("SELECT * FROM reportes LIMIT ?, ?", (ubicacion, fin))
    return res.fetchall()

def conseguir_reporte(id):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM reportes WHERE id = ?", (id,))
    return res.fetchone()

def crear_usuario(nombre, email, clave, nivel):
    cursor = db.cursor()
    res = cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)", (nombre, email, clave, nivel))

def conseguir_usuario(email):
    cursor = db.cursor()
    res = cursor.execute("SELECT * from usuarios WHERE email = ?", (email,))
    return res.fetchone()

def actualizar_nivel(email, nivel):
    cursor = db.cursor()
    res = cursor.execute("UPDATE usuarios SET nivel = ? WHERE email = ?", (nivel, email))

def actualizar_clave(email, clave):
    cursor = db.cursor()
    res = cursor.execute("UPDATE usuarios SET clave = ? WHERE email = ?", (clave, email))

def eliminar_usuario(email):
    cursor = db.cursor()
    cursor.execute("DELETE FROM reportes WHERE email = ?", (email,))

def crear_codigo(email, codigo, tipo):
    cursor = db.cursor()
    res = cursor.execute("INSERT INTO codigos VALUES (?, ?, ?)", (email, codigo, tipo))

def conseguir_codigo(codigo):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM codigos WHERE codigo = ?", (codigo,))
    return res.fetchone()

def eliminar_codigo(codigo):
    cursor = db.cursor()
    res = cursor.execute("DELETE FROM codigos WHERE codigo = ?", (codigo,))
