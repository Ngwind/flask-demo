import functools
from flask import Blueprint

bp = Blueprint("auth", import_name=__name__, url_prefix="/auth")
