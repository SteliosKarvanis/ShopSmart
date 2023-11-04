import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# Create blueprint for views used in recommendation logic

bp = Blueprint("server", __name__, url_prefix="/server")


@bp.route("/search-product-type", methods=("GET", "POST"))
def search_product_type():
    if "GET" == request.method:
        return "Request received, response sent."


@bp.route("/recommend-markets", methods=("GET", "POST"))
def recommend_markets():
    if "GET" == request.method:
        return "Request received, response sent."


@bp.route("/search-alternative-product-instances", methods=("GET", "POST"))
def search_alternative_product_instances():
    if "GET" == request.method:
        return "Request received, response sent."
