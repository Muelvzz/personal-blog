from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=["POST", "GET"])
@login_required
def create_post():

    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Your post has no content", category="error")

        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()

            flash("Your post is created", category="success")
            
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)

@views.route("/delete-post/<get_id>")
@login_required
def delete_post(get_id):

    post = Post.query.filter_by(id=get_id).first()
    if not post:
        flash("Post does not exist", category="error")

    elif current_user.id != post.id:
        flash("You do not have permission to delete the post", category="error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post successfully delete", category="success")

    return redirect(url_for("views.home"))
