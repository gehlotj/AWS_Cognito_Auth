from flask import Blueprint

homepage_bp = Blueprint('homepage_bp',__name__,template_folder='templates',static_folder='static')

@homepage_bp.route('/homepage')
def homepage():
    return render_template("homepage.html")
