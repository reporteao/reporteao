from reporteao import db
import pytest

def f():
    db.init()

def test_answer():
    assert f() == None
