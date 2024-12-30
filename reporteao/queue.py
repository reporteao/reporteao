from . import config, db
from huey import SqliteHuey
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

conf = config.cargar_configuracion('config.toml')
cola = SqliteHuey(filename=conf['base']['queue'])
contexto = ssl.create_default_context()

@cola.task()
def enviar_correo(destinatario, asunto, texto):
    host = conf['email']['host']
    puerto = conf['email']['port']
    direccion = conf['email']['address']
    username = conf['email']['username']
    clave = conf['email']['password']

    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = asunto
    mensaje['From'] = direccion
    mensaje['To'] = destinatario
    mensaje.attach(MIMEText(texto, 'plain', 'utf-8'))

    with smtplib.SMTP_SSL(host, puerto, context=contexto) as servidor:
        servidor.login(username, clave)
        servidor.sendmail(direccion, destinatario, mensaje.as_string())
        servidor.quit()

@cola.task()
def expirar_codigo(id):
    codigo = db.conseguir_codigo(id)
    if codigo:
        if codigo[2] == 0:
            db.eliminar_usuario(codigo[0])
        db.eliminar_codigo(codigo)

