import functools
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint("auth", import_name=__name__, url_prefix="/auth")


@bp.route(rule="/register", methods=["GET", "POST", ])
def register():
    if request.method == "POST":
        username = request.form.get(key="username", default=None)
        password = request.form.get(key="password", default=None)
        db = get_db()
        error = None
        if not username:
            error = "Username is required!"
        if not password:
            error = "Password is required!"

        if error is None:
            try:
                sql = "INSERT INTO user (username, password) VALUES (?, ?)"
                db.execute(
                    sql, (username, generate_password_hash(str(password))))
                db.commit()
            except db.IntegrityError:
                error = "User {} is already registered.".format(username)
            else:  # 已注册用户，重定向到登录页面
                return redirect(location=url_for("auth.login"))

        flash(str(error))

    return render_template("auth/register.html")


@bp.route(rule="login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # 执行登录
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"
            
        if error is None:  # session 中保存登录状态，重定向到欢迎页面
            session.clear()
            session["user_id"] = user["id"]
            flash("Log in success.")
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("auth/login.html")  # get方法返回登录页面


@bp.route(rule="/logout")
def logout():  # 执行注销登录，重定向到欢迎页面
    session.clear()
    flash("Log out success.")
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():  # 每次请求之前检查session中的user.id ,检查是否已经登录，并将信息保存在g对象中。
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        ).fetchone()


def login_required(view):  # 一个装饰器，给其他需要登录的view函数使用。验证有没有登录
    @functools.wraps(view)
    def _view(**kwargs):
        if g.user is None:
            flash("You need to log in.")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return _view
