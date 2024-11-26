import smtplib, ssl

contexto = ssl.create_default_context()

def enviar_correo(destinatario, texto, config):
    host = config['email']['host']
    puerto = config['email']['port']
    direccion = config['email']['address']
    clave = config['email']['password']

    with smtplib.SMTP_SSL(host, puerto, context=contexto) as servidor:
        servidor.login(direccion, clave)
        servidor.sendmail(direccion, destinatario, texto)
        
