from flask import Flask
from .routes import bp
from . import db, config

# Inicializa la base de datos
db.init()

# Carga la llave secreta
conf = config.cargar_configuracion('config.toml')
secreto = conf['base']['secret']

# Configura la app
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '../upload/'

app = Flask(__name__,static_folder='../static/css')
app.secret_key = secreto
app.register_blueprint(bp)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

if __name__ == '__main__':
    app.run()
