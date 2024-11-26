from flask import Flask
from .routes import bp
from . import db, config

# Inicializa la base de datos
db.init()

app = Flask(__name__)

app.register_blueprint(bp)
