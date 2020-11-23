from flask import render_template, Blueprint, jsonify
from flask import current_app as app
from werkzeug.exceptions import HTTPException
import json
import logging
# Create or get the logger
logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)

error_bp = Blueprint('error_bp',__name__,template_folder = 'templates',static_folder='static')

@app.errorhandler(Exception)
def handle_error(e):
    description = e
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
        description = e.description
    logger.error("{0} : {1}".format(code,description))
    return render_template("error.html",code = code, message = description)
