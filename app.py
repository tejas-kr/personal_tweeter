from flask import Flask, jsonify, render_template
from decouple import config

from .authentication import auth
from .main_functions import m_func

app = Flask(__name__)
app.config["SECRET_KEY"] = config("FLASK_SECRET")

app.register_blueprint(auth)
app.register_blueprint(m_func)

if __name__ == "__main__":
    app.run()