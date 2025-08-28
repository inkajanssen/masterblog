import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_blog_posts():
    try:
        with open("data/blog_post_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_blog_posts(entry: dict):
    blog_posts = load_blog_posts()
    blog_posts.append(entry)

    with open("data/blog_post_data.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file)


def delete_blog_post(new_blog_posts:list):

    with open("data/blog_post_data.json", "w", encoding="utf-8") as file:
        json.dump(new_blog_posts, file)

def update_blog_post(new_blog_post:dict):
    blog_posts = load_blog_posts()

    for post in blog_posts:
        if post.get('id') == new_blog_post.get('id'):
            post['author'] = new_blog_post.get('author')
            post['title'] = new_blog_post.get('title')
            post['content'] = new_blog_post.get('content')
            break

    with open("data/blog_post_data.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file)


def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post_id == post.get('id'):
            return post
    return f"{post_id} not found in the blog posts"


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_id = len(blog_posts) + 1

        new_post = {"id": blog_id, "author": author, "title": title, "content": content}
        save_blog_posts(new_post)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post.get('id') != post_id ]
    delete_blog_post(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
    # Update the post in the JSON file
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        updated_post = {"id": post['id'], "author": author, "title": title, "content": content}
        update_blog_post(updated_post)

    # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
