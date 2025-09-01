import json
import os.path

DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(DIR, "blog_post_data.json")


def load_blog_posts():
    """
    Load the Json Data
    :return:
    """
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_blog_posts(entry: dict):
    """
    Saves a new post at the end of the JSON data
    :param entry:
    :return:
    """
    blog_posts = load_blog_posts()
    blog_posts.append(entry)

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(blog_posts, file)


def delete_blog_post(new_blog_posts:list):
    """
    Saves after deleting a post
    :param new_blog_posts:
    :return:
    """
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(new_blog_posts, file)


def update_blog_post(new_blog_post:dict):
    """
    Updates a post and saves it
    :param new_blog_post:
    :return:
    """
    blog_posts = load_blog_posts()

    for post in blog_posts:
        if post.get('id') == new_blog_post.get('id'):
            post['author'] = new_blog_post.get('author')
            post['title'] = new_blog_post.get('title')
            post['content'] = new_blog_post.get('content')
            break

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(blog_posts, file)


def fetch_post_by_id(post_id):
    """
    Fetches post by id
    :param post_id:
    :return:
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post_id == post.get('id'):
            return post
    return f"{post_id} not found in the blog posts"