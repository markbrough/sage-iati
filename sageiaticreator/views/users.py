from flask import Flask, render_template, flash, request, Markup, \
    session, redirect, url_for, escape, Response, abort, send_file, \
    current_app
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login,
                            fresh_login_required)
                            
from sageiaticreator import app, db, models
from sageiaticreator.query import user as quser

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return quser.user(id)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        user = quser.user_by_username(request.form["username"])
        if (user and user.check_password(request.form["password"])):
            if login_user(user):
                flash("Logged in!", "success")
                if request.args.get("next"):
                    redir_url = request.script_root + request.args.get("next")
                else:
                    redir_url = url_for("dashboard")
                return redirect(redir_url)
            else:
                flash("Sorry, but you could not log in.", "error")
        else:
            flash(u"Invalid username or password.", "error")
    return render_template("login.html",
             loggedinuser=current_user)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    redir_url = url_for("dashboard")
    return redirect(redir_url)