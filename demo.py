from flask import Flask, url_for, request, make_response, redirect, abort
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route(rule="/test_methods/<string:name>", methods=["GET", ])
def hello_user(name):
    return "<p>Hello {}!</p>".format(name)


@app.route("/test_url_for/<string:func_name>")
def demo_url_for(func_name):
    return "This is url for {}".format(url_for(endpoint=func_name, func_name=func_name))


@app.route("/test_request/", methods=["GET", "POST", "PUT", "DELETE", "HEAD"])
def demo_request():
    return request.method


@app.route("/test_args/", methods=["POST", "GET"])
def demo_get_args():
    return request.args


@app.route("/test_upload_file/", methods=["POST"])
def demo_upload_file():
    app.logger.warning([str(i) for i in request.files.keys()])
    file_ = request.files["the_file"]
    file_.save("./{}".format(secure_filename(file_.filename)))  # type: ignore
    return ""


@app.route("/test_cookies/")
def demo_get_set_cookies():
    resp = make_response("，".join(request.cookies.keys()))
    resp.set_cookie(key="flask_set_ckey", value="这是falsk设置的cookies")
    return resp


@app.route("/test_redirect/")
def demo_redirect():
    resp = redirect(location=url_for("hello_world"))
    return resp

@app.route("/test_abort/")
def demo_abort():
    abort(status=404)
    return "?"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
