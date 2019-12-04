from flask import Blueprint, render_template
from flask_login import current_user

from sageiaticreator.extensions import db
from sageiaticreator import models
from sageiaticreator import setup as sisetup
from sageiaticreator.views import users, organisations, activities, generate
from sageiaticreator.query import organisation as siorganisation


app = Blueprint('routes', __name__,
    url_prefix='/', static_folder='../static')


@app.route("/")
def dashboard():
    organisations = siorganisation.list_orgs()
    return render_template("home.html",
                organisations = organisations,
                loggedinuser=current_user
                          )

@app.route("/setup/")
def setup():
    sisetup.setup()
    return "OK"
