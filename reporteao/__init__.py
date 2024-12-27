from flask import Flask
from .routes import bp
from . import db, config

# Inicializa la base de datos
db.init()

# Carga la llave secreta
conf = config.cargar_configuracion('config.toml')
secreto = conf['base']['secret']

# Configura la app
app = Flask(__name__,static_folder='/workspaces/reporteao/static/css')
app.secret_key = secreto
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()