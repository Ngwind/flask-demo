from flask import Blueprint, render_template, url_for, request, flash, redirect, g, abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", import_name=__name__, url_prefix="/blog")


@bp.route(rule="/")
@login_required
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id,title,body,create_time,author_id,username"
        " FROM post AS p JOIN user as u ON p.author_id = u.id"
        " ORDER BY create_time DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route(rule="/create", methods=["GET", "POST", ])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, create_time, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route(rule="/update/<int:id>", methods=["GET", "POST", ])
@login_required
def update(id):
    post = get_post(id)
    if  request.method == "POST":
        title=request.form["title"]
        body=request.form["body"]
        error = None

        if not title:
            error = "Title is required!"
            flash(error)
        else:
            db = get_db()
            db.execute(
                "update post set title = ?, body = ?"
                "where id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html",post=post)

@bp.route(rule="/delete/<int:id>",methods=["POST"])
@login_required
def delete(id):
    get_post(id)
    db= get_db()
    db.execute(
        "delete from post where id = ?",
        (id,)
    )
    db.commit()
    return redirect(url_for("blog.index"))