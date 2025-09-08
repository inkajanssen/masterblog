import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from data import *

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


def input_validation(author, title, content):
    if not author or not title or not content:
        return False
    return True



@app.route('/')
def index():
    """
    This route will display all blog posts.
    It links to add another post.
    Gives the option to update or delete a post
    :return:
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    A route to our blog application that will allow us to add a new blog post
    :return:
    """
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        author = request.form.get('author').strip()
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()

        if not input_validation(author,title, content):
            flash("You need to fill out every field")
            return redirect(url_for('add'))

        # load last blog_post id and add 1
        blog_id = blog_posts[-1]['id'] + 1
        new_post = {"id": blog_id, "author": author, "title": title,
                    "content": content}
        save_blog_posts(new_post)

        return redirect(url_for('index'))

    return render_template('add.html', author='', title='', content='')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
     A route to handle the deletion of blog posts
    :param post_id:
    :return:
    """
    blog_posts = load_blog_posts()
    # Find the blog post with the given id and remove it from the list
    blog_posts = [post for post in blog_posts if post.get('id') != post_id ]
    delete_blog_post(blog_posts)
    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Add a route to update an existing blog post
    :param post_id:
    :return:
    """
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

        if not input_validation(author, title, content):
            redirect(url_for('update', post_id=post_id))

        updated_post = {"id": post['id'], "author": author, "title": title, "content": content}
        update_blog_post(updated_post)

    # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
