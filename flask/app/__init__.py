from flask import Flask
from flask.ext.bootstrap import Bootstrap

from config import config

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .ajax import ajax as ajax_blueprint
    app.register_blueprint(ajax_blueprint, url_prefix='/ajax')


    """
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    from .report import report as report_blueprint
    app.register_blueprint(report_blueprint, url_prefix='/report')
    """

    return app
