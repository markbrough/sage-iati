from flask import Flask, render_template, flash, request, Markup, \
    session, redirect, url_for, escape, Response, abort, send_file, jsonify
from flask.ext.login import login_required, current_user

from sageiaticreator import app
from sageiaticreator import db
import models
import setup as sisetup
from views import users, organisations, activities, generate
from query import organisation as siorganisation

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
