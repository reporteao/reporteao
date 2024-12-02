from flask import Blueprint, request, session
from argon2 import PasswordHasher
from jinja2 import Environment, PackageLoader, select_autoescape
from .email import enviar_correo
from . import db, config, util

templateEnv = Environment(
    loader=PackageLoader('reporteao', '../templates'),
    autoescape=select_autoescape()
)
bp = Blueprint("routes", __name__)
conf = config.cargar_configuracion('config.toml')
ph = PasswordHasher()

@bp.route('/')
def inicio():
    reportes = db.listar_reportes(1)
    # TODO(NecroBestia): Agregar vista principal
    return reportes

# Requiere un método POST con los siguientes parámetros:
# - 'email': Correo del usuario, sin @usach.cl. Ejemplo: john.doe
# - 'clave': Contraseña del usuario
# En caso de no ser una solicitud POST, debe retornar el formulario de login
@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # NOTA: Al hacer el formulario, este campo debería señalar de que el @usach.cl ya está presente.
        email = str(request.form['email']) + '@usach.cl'

        # Se busca el usuario en la base de datos
        usuario = db.conseguir_usuario(email)

        # Se verifica si existe el usuario
        if not usuario:
            return "Usuario no existe"

        # Se verifica si el usuario ya fue verificado o no
        if usuario[3] < 0:
            return "Usuario no está habilitado para iniciar sesión"
            
        # Se verifica si la contraseña es válida
        try:
            ph.verify(usuario[2], str(request.form['clave']))
        except argon2.exceptions.VerifyMismatchError:
            return "Contraseña inválida"
        
        # Se inicia sesión
        session['usuario'] = email
        # TODO: Redireccionar a la página principal
        return "Sesión iniciada"
    # TODO(NecroBestia): Formulario de login
    return "TODO"

# Requiere un método POST con los siguientes parámetros:
# - 'nombre': Nombre real de lx usuarix. Ejemplo: John Doe
# - 'email': Correo de lx usuarix, sin @usach.cl. Ejemplo: john.doe
# - 'clave': Contraseña de lx usuarix
# - 'clave2': Contraseña de lx usuarix, repetida
# En caso de no ser una solicitud POST, debe retornar el formulario de registro
@bp.route('/register', methods = ['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        # Se consiguen los datos desde el formulario
        nombre = str(request.form['nombre'])
        # TODO(otoayana): Validar si el correo está bien escrito
        email = str(request.form['email']) + '@usach.cl'
        clave = ph.hash(str(request.form['clave']))

        # Se invalida la solicitud si las contraseñas no son iguales
        if request.form['clave'] != request.form['clave2']:
            return "Contraseñas no coinciden"

        # Se crea el usuario
        db.crear_usuario(nombre, email, clave, -1)

        # Se crea el código de verificación
        codigo = util.uuid()
        db.crear_codigo(email, codigo, 0)

        # Se envía el código de verificación por email al usuario
        plantilla = templateEnv.get_template('email/verificacion.txt')
        correo = plantilla.render(uri=conf['web']['uri'], codigo=codigo)
        enviar_correo(email, 'Verifique su cuenta de ReportEAO', correo)

        return "Se ha enviado un enlace de verificación a su correo institucional. Haga click en él para terminar de crear su cuenta."
    else:
        # TODO(NecroBestia): Agregar formulario de registro
        return "TODO"

@bp.route('/add')
def agregar_reporte():
    return "TODO"

@bp.route('/like/<id>')
def apoyar_reporte(id):
    if session.has_key('usuario'):
        db.crear_apoyo(session['usuario'], id)
    else:
        return "Sesión no iniciada"

@bp.route('/solve/<id>')
def resolver_reporte(id):
    if session.has_key('usuario'):
        usuario = db.conseguir_usuario(session['usuario'])
        if usuario[3] > 1:
            db.actualizar_reporte(id, 1)
        else:
            return "No estás autorizadx para realizar esta operación"
    else:
        return "Sesión no iniciada"

@bp.route('/delete/<id>')
def eliminar_reporte(id):
    if session.has_key('usuario'):
        usuario = db.conseguir_usuario(session['usuario'])
        if usuario[3] > 2:
            db.eliminar_reporte(id)
        else:
            return "No estás autorizadx para realizar esta operación"
    else:
        return "Sesión no iniciada"

@bp.route('/verify')
def verificar():
    return "TODO"
