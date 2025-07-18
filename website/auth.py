from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return "this is the login page"

@auth.route("/sign-up")
def sign_up():
    return "this is the sign-up page"

@auth.route("/log-out")
def log_out():
    return "this is the log-out page"