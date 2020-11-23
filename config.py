from os import environ,path
from dotenv import load_dotenv
import datetime

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir,'.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SESSION_TYPE = environ.get('SESSION_TYPE')#session configuration
    CLIENT_ID = environ.get('CLIENT_ID')
    REDIRECT_URI = environ.get('REDIRECT_URI')
    CLIENT_AUTH = environ.get('CLIENT_AUTH')
    LOGIN_URL = environ.get('LOGIN_URL')
    TOKEN_URL = environ.get('TOKEN_URL')
    USER_INFO_ENDPOINT = environ.get('USER_INFO_ENDPOINT')
    PUBLIC_KEY_URL = environ.get('PUBLIC_KEY_URL')
    REGION = environ.get('REGION')
    POOL_ID = environ.get('POOL_ID')

    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')#jwt token configuration
    JWT_COOKIE_CSRF_PROTECT = environ.get('JWT_COOKIE_CSRF_PROTECT')
    JWT_CSRF_CHECK_FORM = environ.get('JWT_CSRF_CHECK_FORM')
    JWT_TOKEN_LOCATION = environ.get('JWT_TOKEN_LOCATION')
    JWT_DECODE_ALGORITHMS = environ.get('JWT_DECODE_ALGORITHMS')
    JWT_PUBLIC_KEY = environ.get('JWT_PUBLIC_KEY')
    JWT_ALGORITHM = environ.get('JWT_ALGORITHM')
    JWT_IDENTITY_CLAIM = environ.get('JWT_IDENTITY_CLAIM')
