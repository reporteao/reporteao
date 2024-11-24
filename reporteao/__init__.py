from flask import Flask
from .routes import bp
from .db import init

init()

app = Flask(__name__)

app.register_blueprint(bp)
