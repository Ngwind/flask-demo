import functools
from flask import Blueprint, request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash
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
