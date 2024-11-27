import sqlite3
from . import config

"""
    Este archivo define abstracciones para comandos de SQLite, para así
    facilitar las interacciones dentro del programa.
"""

conf = config.cargar_configuracion('config.toml')
archivo = conf['base']['database']

# Inicializa la base de datos
def init():
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS reportes(autor, titulo, facultad, descripcion, imagenes, fecha, likes, estado)")
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(nombre, email, clave, nivel)")
        cursor.execute("CREATE TABLE IF NOT EXISTS codigos(email, codigo, tipo)")
        db.commit()

def agregar_reporte(autor, titulo, facultad, descripcion, imagenes):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO reportes VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (autor, titulo, facultad, descripcion, imagenes, 0, 0))
        db.commit()

def eliminar_reporte(id):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM reportes WHERE id = ?", (id,))
        db.commit()

def actualizar_reporte(id, estado):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        cursor.execute("UPDATE reportes SET estado = ? WHERE id = ?", (estado, id))
        db.commit()

def listar_reportes(ubicacion):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        fin = ubicacion + 20
        res = cursor.execute("SELECT * FROM reportes LIMIT ?, ?", (ubicacion, fin))
        db.commit()
        return res.fetchall()

def conseguir_reporte(id):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("SELECT * FROM reportes WHERE id = ?", (id,))
        db.commit()
        return res.fetchone()

def crear_usuario(nombre, email, clave, nivel):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)", (nombre, email, clave, nivel))
        db.commit()

def conseguir_usuario(email):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("SELECT * from usuarios WHERE email = ?", (email,))
        db.commit()
        return res.fetchone()

def actualizar_nivel(email, nivel):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("UPDATE usuarios SET nivel = ? WHERE email = ?", (nivel, email))
        db.commit()

def actualizar_clave(email, clave):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("UPDATE usuarios SET clave = ? WHERE email = ?", (clave, email))
        db.commit()

def eliminar_usuario(email):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM reportes WHERE email = ?", (email,))
        db.commit()

# Crea un código de verificación. El tipo de código se define como un
# entero equivalente a los siguientes valores:
# - 0: Código de verificación de cuenta
# - 1: Código de reestablecimiento de clave
def crear_codigo(email, codigo, tipo):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("INSERT INTO codigos VALUES (?, ?, ?)", (email, codigo, tipo))
        db.commit()

def conseguir_codigo(codigo):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("SELECT * FROM codigos WHERE codigo = ?", (codigo,))
        db.commit()
        return res.fetchone()

def eliminar_codigo(codigo):
    with sqlite3.connect(archivo) as db:
        cursor = db.cursor()
        res = cursor.execute("DELETE FROM codigos WHERE codigo = ?", (codigo,))
        db.commit()
