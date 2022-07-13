
from flask import Flask,url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route(rule="/<string:name>",methods=["GET",])
def hello_user(name):
    return "<p>Hello {}!</p>".format(name)


@app.route("/<name>",methods=["POST",])
def add_user(name):
    return "<p>Hello {}!</p>".format(name)

@app.route("/url_for/<string:func_name>")
def demo_url_for(func_name):
    return "This is url for {}".format(url_for(endpoint=func_name,func_name=func_name))

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
