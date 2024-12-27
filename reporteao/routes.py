from flask import Blueprint, request, session, render_template, send_from_directory
from argon2 import PasswordHasher
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from .email import enviar_correo
from . import db, config, util
import pdb

templateEnv = Environment(
    loader=PackageLoader('reporteao', '../templates/', encoding='utf-8'),
    autoescape=select_autoescape()
)
bp = Blueprint("routes", __name__)
conf = config.cargar_configuracion('config.toml')
ph = PasswordHasher()

bp.jinja_loader = FileSystemLoader('/workspaces/reporteao/templates/')

@bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(bp.static_folder, filename)

# Rutas de la aplicación
@bp.route('/')
def inicio():
    reportes = db.listar_reportes(1)
    # TODO: Agregar vista principal
    return render_template('index.html', reportes=reportes)


# Requiere un método POST con los siguientes parámetros:
# - 'email': Correo del usuario, sin @usach.cl. Ejemplo: john.doe
# - 'clave': Contraseña del usuario
# En caso de no ser una solicitud POST, debe retornar el formulario de login
@bp.route('/login', methods=['POST', 'GET'])
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
        return "Sesión iniciada"
    else:
        return render_template('LogIn.html')

# Requiere un método POST con los siguientes parámetros:
# - 'nombre': Nombre real de lx usuarix. Ejemplo: John Doe
# - 'email': Correo de lx usuarix, sin @usach.cl. Ejemplo: john.doe
# - 'clave': Contraseña de lx usuarix
# - 'clave2': Contraseña de lx usuarix, repetida
# En caso de no ser una solicitud POST, debe retornar el formulario de registro
@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Se consiguen los datos desde el formulario
        nombre = str(request.form['nombre'])
        # TODO: Validar si el correo está bien escrito
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
        # TODO: Agregar formulario de registro
        return render_template('SingUp.html', title='Registrarse')

@bp.route('/add')
def agregar_reporte():
    return "TODO"

@bp.route('/like/<id>')
def apoyar_reporte(id):
    if 'usuario' in session:
        apoyos = db.conseguir_apoyos(id)
        existe = False
        i = 0
        while i < len(apoyos) or not existe:
            if apoyos[i][0] == session['usuario']:
                existe = True
                
        if not existe:
            db.crear_apoyo(session['usuario'], id)
        else:
            db.eliminar_apoyo(session['usuario'], id)
    else:
        return "Sesión no iniciada"

@bp.route('/solve/<id>')
def resolver_reporte(id):
    if 'usuario' in session:
        usuario = db.conseguir_usuario(session['usuario'])
        if usuario[3] > 1:
            db.actualizar_reporte(id, 1)
        else:
            return "No estás autorizadx para realizar esta operación"
    else:
        return "Sesión no iniciada"

@bp.route('/delete/<id>')
def eliminar_reporte(id):
    if 'usuario' in session:
        usuario = db.conseguir_usuario(session['usuario'])
        reporte = db.conseguir_reporte(id)
        
        # Eliminar el reporte si lx usuarix es dueñx
        if usuario[3] > 2 or reporte[1] == usuario[0]:
            db.eliminar_reporte(id)
        else:
            return "No estás autorizadx para realizar esta operación"
    else:
        return "Sesión no iniciada"

@bp.route('/verify/<id>')
def verificar(id):
    codigo = db.conseguir_codigo(id)

    if not codigo:
        return "Código no encontrado"
    
    if codigo[2] == 0:
        usuario = db.actualizar_nivel(codigo[0], 0)
        return "Usuario activado"
    
    if codigo[2] == 1:
        # TODO: Agregar sistema de reestablecimiento de claves
        return "TODO"