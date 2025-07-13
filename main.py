from flask import Flask, redirect, url_for, render_template, abort
import frontmatter
import markdown
import glob
import os

app = Flask(__name__)

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

@app.route("/")
def home():
    posts = load_post()
    return render_template("index.html", article=posts)

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

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)