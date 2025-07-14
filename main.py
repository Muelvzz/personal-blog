from flask import Flask, redirect, url_for, render_template, abort, request, flash, session
from functools import wraps
import frontmatter
import markdown
import glob
import os
from datetime import datetime
import os

time = datetime.now()
folder_path = r"C:\Programming\Projects\Personal_Blog\articles"

app = Flask(__name__)

"""
    Admin Processing
"""

# Admin authentication
app.secret_key = "your_secret_key"

USERNAME = "admin"
PASSWORD = "secret"

@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("invalid credentials")

    return render_template("login.html")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

"""
    Article Loadings
"""

# Loading written articles into the web
def load_post():

    posts = []

    for filepath in glob.glob("articles/*.md"):
        post = frontmatter.load(filepath)

        slug = os.path.splitext(os.path.basename(filepath))[0]
        title = post['title']
        date = post['date']
        content_html = markdown.markdown(post.content)

        posts.append({"slug": slug,
                    "title": title,
                    "date": date,
                    "content_html": content_html
                    })
        
    return posts

@app.route("/article/<string:get_slug>")
def article_detail(get_slug):
    all_posts = load_post()
    found_post = None
    for post in all_posts:
        if post['slug'] == get_slug:
            found_post = post
            break

    if found_post:
        return render_template("article_detail.html", post=found_post)
    else:
        abort(404)

"""
    Websites
"""

@app.route("/")
def home():
    posts = load_post()
    return render_template("index.html", article=posts)


"""
    Admin Website
"""

@app.route("/admin")
@login_required
def admin_dashboard():
    posts = load_post()
    return render_template("admin.html", article=posts)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_article():

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        current_date = time.strftime("%B %d, %Y")

        file_number = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]) + 1
        file_name = f"article{file_number}.md"

        file_path = os.path.join(folder_path, file_name)

        file_content = f"""---
title: {title}
date: {current_date}
---

{content}
        """

        with open(file_path, "w") as file:
            file.write(file_content)

    return render_template("add_article.html")

if __name__ == "__main__":
    app.run(debug=True)