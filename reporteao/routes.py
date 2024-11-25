from flask import Blueprint

bp = Blueprint("routes", __name__)

@bp.route('/')
def inicio():
    return "TODO"

@bp.route('/login')
def login():
    return "TODO"

@bp.route('/register')
def registrar():
    return "TODO"

@bp.route('/add')
def agregar_reporte():
    return "TODO"

@bp.route('/like')
def apoyar_reporte():
    return "TODO"

@bp.route('/solve')
def resolver_reporte():
    return "TODO"

@bp.route('/delete')
def eliminar_reporte():
    return "TODO"
