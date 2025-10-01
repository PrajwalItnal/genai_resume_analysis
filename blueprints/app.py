from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='template')
    app.secret_key = 'Prajwal@123'

    from .core.routes import core
    app.register_blueprint(core,url_prefix='/')
    from .Resume_analyse.routes import analyse
    app.register_blueprint(analyse,url_prefix='/analyse')

    return app