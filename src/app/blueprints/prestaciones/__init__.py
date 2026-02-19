from flask import Blueprint

bp = Blueprint("prestaciones", __name__, template_folder="templates")

from . import routes