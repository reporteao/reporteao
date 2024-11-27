import smtplib, ssl
from . import config
from huey import SqliteHuey

conf = config.cargar_configuracion('config.toml')
cola = SqliteHuey(filename=conf['base']['queue'])
contexto = ssl.create_default_context()

@cola.task()
def enviar_correo(destinatario, texto):
    host = conf['email']['host']
    puerto = conf['email']['port']
    direccion = conf['email']['address']
    clave = conf['email']['password']

    with smtplib.SMTP_SSL(host, puerto, context=contexto) as servidor:
        servidor.login(direccion, clave)
        servidor.sendmail(direccion, destinatario, texto)
