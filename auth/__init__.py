from flask import Flask,abort
from flask_session import Session
from auth.models import jwt_manager
from auth.helper import Req
import logging
from logging import handlers

sess = Session()
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    sess.init_app(app)
    with app.app_context():
        from .login import login
        from .homepage import homepage
        from .errors import error

        #configuring jwt token. Env file doesnt have a method to
        #read boolean operator
        #.env file
        if app.config.get('JWT_COOKIE_CSRF_PROTECT') == 'True':
            app.config['JWT_COOKIE_CSRF_PROTECT'] = True
        else: app.config['JWT_COOKIE_CSRF_PROTECT'] = False

        if app.config.get('JWT_CSRF_CHECK_FORM') == 'True':
             app.config['JWT_CSRF_CHECK_FORM'] = True
        else: app.config['JWT_CSRF_CHECK_FORM'] = False

        jwt_manager.init_app(app)
        #registering the blueprint
        app.register_blueprint(login.login_bp)
        app.register_blueprint(homepage.homepage_bp)
        app.register_blueprint(error.error_bp)

        #registering the log handler
        handler = logging.handlers.RotatingFileHandler('app.log',maxBytes=1024 * 1024)
        handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(lineno)s - %(funcName)s :-> %(message)s')
        handler.setFormatter(formatter)

        #download public keys
        if not 'JWT_PUBLIC_KEY' in app.config:
            app.logger.error('JWT_PUBLIC_KEY is not defined in env file')
            abort(500)
        app.config['JWT_PUBLIC_KEY'] = Req.get_public_keys(app.config['PUBLIC_KEY_URL'].format(region=app.config['REGION'],userPoolId=app.config['POOL_ID']))

        #encode client id and secret
        if not 'CLIENT_AUTH' in app.config:
            app.logger.error('CLIENT_AUTH is not defined in env file')
            abort(500)
        app.config['CLIENT_AUTH'] = Req.get_encoded_cid(app.config['CLIENT_AUTH'])
        #print(app.config['CLIENT_AUTH'])
        return app
