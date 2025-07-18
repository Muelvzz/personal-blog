from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash("Email is already in use", category="error")
        elif username_exist:
            flash("Username is already in use", category="error")
        elif password1 != password2:
            flash("Password doesn't match", category="error")

        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password1) < 6:
            flash("Password is too short", category="error")
        elif len(email) < 4:
            flash("Email is invalid", category="error")
        else:
            new_user = User(email=email,
                            username=username,
                            password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User is created")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("views.home"))