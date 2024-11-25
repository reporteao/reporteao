from reporteao import db
import pytest

def f(nombre, email, clave, nivel):
    db.init()
    db.crear_usuario(nombre, email, clave, nivel)
    return db.conseguir_usuario(email)

def test_answer():
    assert f("John Doe", "john@example.com", "PLACEHOLDER", -1) == ("John Doe", "john@example.com", "PLACEHOLDER", -1)
