import sqlite3

db = sqlite3.connect("database.db")

# Inicializa la base de datos
def init():
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS reportes(autor, titulo, facultad, descripcion, imagenes, fecha, likes, estado)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios(nombre, email, clave, nivel)")

def agregar_reporte(autor, titulo, facultad, descripcion, imagenes):
    cursor.execute("INSERT INTO reportes VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (autor, titulo, facultad, descripcion, imagenes, 0, 0))
    pass

def eliminar_reporte(id):
    pass

def actualizar_reporte(id, estado):
    pass

def listar_reportes(cursor):
    pass

def conseguir_reporte(id):
    pass

def crear_usuario(nombre, email, clave, nivel):
    pass

def conseguir_usuario(email):
    pass

def eliminar_usuario(email):
    pass
