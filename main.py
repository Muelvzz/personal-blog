from flask import Flask, redirect, url_for, render_template, abort, request, flash, session
from functools import wraps
import frontmatter
import markdown
import glob
import os

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

@app.route("/admin")
@login_required
def admin_dashboard():
    posts = load_post()
    return render_template("admin.html", article=posts)

if __name__ == "__main__":
    app.run(debug=True)