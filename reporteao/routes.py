from flask import Blueprint, request, session, render_template, redirect, flash
from argon2 import PasswordHasher
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from .queue import enviar_correo, expirar_codigo
from . import db, config, util
from datetime import datetime
from werkzeug.utils import secure_filename


templateEnv = Environment(
    loader=PackageLoader('reporteao', '../templates/', encoding='utf-8'),
    autoescape=select_autoescape()
)
bp = Blueprint("routes", __name__, static_folder='../static/')
conf = config.cargar_configuracion('config.toml')
ph = PasswordHasher()

bp.jinja_loader = FileSystemLoader('./templates/')

# Rutas de la aplicación
@bp.route('/')
def inicio():
    reportes = db.listar_reportes(0)
    usuario = None
    if 'usuario' in session:
        usuario = db.conseguir_usuario(session['usuario'])
    
    return render_template('index.html', reportes=reportes,usuario=usuario)


################################## Sesion ##################################
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
            flash('Usuario no existe')
            return redirect('/login', code=302)

        # Se verifica si el usuario ya fue verificado o no
        '''if usuario[3] < 0:
            flash('Usuario no está habilitado para iniciar sesión')
            return redirect('/login', code=302)'''
            
        # Se verifica si la contraseña es válida
        try:
            ph.verify(usuario[2], str(request.form['clave']))
        except argon2.exceptions.VerifyMismatchError:
            flash('Contraseña inválida')
            return redirect('/login', code=302)
        
        # Se inicia sesión
        session['usuario'] = email
        flash('Sesión iniciada')
        return redirect('/', code=302)
    else:
        return render_template('login.html')

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
        clave = ph.hash(str(request.form['clave']))

        # Valida si el correo está bien escrito
        for char in request.form['email']:
            if not ((char.isalpha() and char.islower()) or char == '.'):
                flash('Correo no válido')
                return redirect('/register', code=302)
        email = str(request.form['email']) + '@usach.cl'
        usuarioExistente = db.conseguir_usuario(email)
        
        if usuarioExistente:
            flash('Usuario ya existe')
            return redirect('/register', code=302)

        # Se invalida la solicitud si las contraseñas no son iguales
        if request.form['clave'] != request.form['clave2']:
            flash('Las contraseñas no coinciden')
            return redirect('/register', code=302)

        # Se crea el usuario
        db.crear_usuario(email, nombre, clave, -1)

        # Se crea el código de verificación
        codigo = util.uuid()
        db.crear_codigo(email, codigo, 0)

        # Se envía el código de verificación por email al usuario
        plantilla = templateEnv.get_template('email/verificacion.txt')
        correo = plantilla.render(uri=conf['web']['uri'], codigo=codigo)
        enviar_correo(email, 'Verifique su cuenta de ReportEAO', correo)
        expirar_codigo.schedule((codigo,), delay=1800)
        flash('Se ha enviado un enlace de verificación a su correo institucional. Haga click en él para terminar de crear su cuenta.')
        return redirect('/login', code=301)
    else:
        return render_template('register.html', title='Registrarse')

@bp.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada')
    return redirect('/', code=302)
################################## Reportes ##################################
@bp.route('/add', methods=['POST', 'GET'])
def agregar_reporte():
    if request.method == 'POST':
        autor = session['usuario']
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        titulo = request.form['report-title']
        sala = request.form['report-room']
        contenido = request.form['report-content']
        
        imagen = request.files['report-image']
        #TODO: Agregar validación de imagen
        if imagen:
            imagen.save(util.uuid())
        else:
            imagen = None
    
        db.agregar_reporte(autor, titulo, sala, contenido, imagen, fecha)
        flash('Reporte creado')
        return redirect('/', code=302)


    else:
        return render_template('crear.html')

@bp.route('/like/<id>')
def apoyar_reporte(id):
    if 'usuario' in session:
        apoyos = db.conseguir_apoyos(id)
        existe = False
        for apo in apoyos:
            if apo[0] == session['usuario']:
                existe = True
                break

        if not existe:
            db.crear_apoyo(session['usuario'], id)
        else:
            db.eliminar_apoyo(session['usuario'], id)

        return redirect('/', code=302)
    else:
        flash('Sesión no iniciada')
        return redirect('/login', code=302)

@bp.route('/solve/<id>')
def resolver_reporte(id):
    if 'usuario' in session:
        usuario = db.conseguir_usuario(session['usuario'])
        if usuario[3] > 1:
            db.actualizar_reporte(id, 1)
            flash('Reporte resuelto')
            return redirect('Adminitracion_reportes', code=302)
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
        if usuario[3] >= 2 or reporte[1] == usuario[0]:
            db.eliminar_reporte(id)
            flash('Reporte eliminado')
            return redirect('/Adminitracion_reportes', code=302)
        else:
            return "No estás autorizadx para realizar esta operación"
    else:
        return "Sesión no iniciada"

#Validacion de cuenta
@bp.route('/verify/<id>')
def verificar(id):
    codigo = db.conseguir_codigo(id)

    if not codigo:
        return "Código no encontrado"
    
    if codigo[2] == 0:
        usuario = db.actualizar_nivel(codigo[0], 0)
    
    # TODO: Agregar opciones para cambiar clave después de iniciar sesión
    if codigo[2] == 1:
        session['usuario'] = codigo[0]

    db.eliminar_codigo(id)
    return redirect('/', code=302)



################################## Cambiar nivel usuario ##################################
@bp.route('/update_nivel/<email>/<int:nivel>', methods=['GET'])
def actualizar_nivel(nivel,email):
        usuario = db.conseguir_usuario(email)        
        db.actualizar_nivel(nivel,email)
        return redirect('/', code=302)


##################################    Admin Panel        ##################################
@bp.route('/Adminitracion_reportes', methods=['GET' , 'POST'])
def admin_reportes():
    reportes=db.listar_reportes(0)
    usuario = db.conseguir_usuario(session['usuario'])
    if usuario[3] >= 2: 
        #nivel 2 o mas es el nivel de administrador
        reportes = db.listar_reportes(0)
    
    elif usuario[3] == 1:
        # Fetch only the reports created by the user for users with level 1
        reportes = db.listar_reportes_por_usuario(usuario[0])
    else:
        flash('No tienes permisos para acceder a esta página')
        return redirect('/', code=302)
                        
    return render_template('admin.html', reportes=reportes)