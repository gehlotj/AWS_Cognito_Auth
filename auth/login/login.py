'''
    The following blueprint serves the login activity of the users request.
'''
import os
import urllib
import hashlib
from flask import render_template, redirect,url_for,request, Blueprint,session, flash, abort, make_response
from flask import current_app as app
from auth.helper import Req
from auth.models import set_access_cookies,jwt_required,jwt_manager,get_jwt_identity
from jose import jwk, jwt
from jose.utils import base64url_decode
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

#configure Blueprint
login_bp = Blueprint('login_bp',__name__,template_folder = 'templates',static_folder = 'static')
service = app.config


@login_bp.route('/')
def login():
    '''
        Entry point of the application
    '''
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state
    params = {"client_id": service['CLIENT_ID'],
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": service['REDIRECT_URI'] }
    url = service['LOGIN_URL'] + urllib.parse.urlencode(params)
    return redirect(url)


@login_bp.route('/callback')
def callback():
    '''
        The following function extract the code from the redirect url and request for id token
    '''
    if request.args.get('state', '') != session['state']:
        flash('Invalid state value.')
        abort(409)
    params = {
        'grant_type':'authorization_code',
        'code':request.args.get('code'),
        'redirect_uri':service['REDIRECT_URI'],
        'client_id': service['CLIENT_ID'],
        'scope': 'open_id email'
    }
    print(service['CLIENT_AUTH'])
    print('above is auth')
    payload = Req.get_token(params,service['CLIENT_AUTH'],service['TOKEN_URL'])
    if payload.status_code == 200:
        url = url_for('login_bp.homepage')
        resp = make_response(redirect(url))
        set_access_cookies(resp, payload.json()["access_token"])
        return resp
    flash('Cannot verify user identity')
    logger.debug(payload.text)
    abort(payload.status_code)


@login_bp.route('/homepage')
@jwt_required
def homepage():
    '''
        This is a function to test the functionality of a authenticated endpoint
    '''
    url = service['USER_INFO_ENDPOINT']
    token = request.cookies.get('access_token_cookie')
    result = Req.auth_post(url,token)
    if result.status_code != 200:
        logger.debug(result.text)
        abort(result.status_code)
    session['username'] = result.json()['email']
    return render_template('homepage.html',email = session['username'])


def get_token():
    '''
        The following method will retrieve the token from stored cookie
    '''
    token = request.cookies.get('access_token_cookie')
    if not token:
        logger.debug("Cannot retrieve token from the cookies. {0}".format(list(request.cookies.keys())))
        abort(500)
    return token


def compare_kid(jwks,token):
    '''
        The following method will compare the current kid from header and match it
        with the public key kid and key signature
    '''
    headers = jwt.get_unverified_headers(token)
    if 'kid' in headers:
        kid = headers['kid']
        key_index = -1
        for i in range(len(jwks)):
            if jwks[i]['kid'] == kid:
                key_index = i
                break
        if key_index == -1:#couldnt match the kid
            logger.debug("jwks variable: {0}".format(jwks))
            raise abort(500,"Cannot find KID from {0}".format(service['PUBLIC_KEY_URL']))
        return key_index
    else:
        logger.debug("Current Heade value: {0}".format(headers))
        return -1

def compare_sig(key,token):
    '''
        The following method will compare key signature
    '''
    message, encoded_signature = str(token).rsplit('.', 1)# decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))# verify the signature
    if not key.verify(message.encode("utf8"), decoded_signature):
        raise abort(400,"Signature mismatch".format(service['PUBLIC_KEY_URL']))
    return True

@jwt_manager.decode_key_loader
def updated_decode_handler(id_token):
    '''
    Reference: https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
    To verify the authentication using RS256 algorithm and cognito public key.
    '''
    jwks = service['JWT_PUBLIC_KEY']
    if not jwks:
        raise abort(500,"Public key unavailable at {0}".format(service['PUBLIC_KEY_URL']))
    token = get_token()
    kid_loc = compare_kid(jwks,token)
    if  kid_loc > -1:
        key = jwk.construct(jwks[kid_loc])
        if compare_sig(key,token):
            return key.to_pem()
        else:
            abort(400)
            logger.error("SIG failed to verify")
    else:
        abort(400)
        logger.error("KID failed to verify")


@jwt_manager.expired_token_loader
def expired_token_callback(callback):
    '''
      Method to handle expired_token
    '''
    flash('Token Expired. Please Login again')
    resp = make_response(redirect(url_for('homepage_bp.homepage')))
    unset_access_cookies(resp)
    return resp


@jwt_manager.unauthorized_loader
def invalid_token_callback(expired_token):
    '''
        Method to handle invalid token
    '''
    flash('Missing Token. Please Login again')
    resp = make_response(redirect(url_for('homepage_bp.homepage')))
    return resp
