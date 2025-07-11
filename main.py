from flask import Flask, redirect, url_for, render_template
import frontmatter
import markdown
import glob
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route("/")
def home():

    posts = []

    for filepath in glob.glob("articles/*.md"):
        post = frontmatter.load(filepath)
        title = post['title']
        date = post['date']
        content_html = markdown.markdown(post.content)

        posts.append({"title": title,
                    "date": date,
                    "content": content_html
                    })

    return render_template("index.html", article=posts)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()