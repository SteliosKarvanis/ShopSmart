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
    jsonify,
)
from . import db as DB
from sqlalchemy import text


# Create blueprint for views used in recommendation logic

bp = Blueprint("server", __name__, url_prefix="/server")


@bp.route("/search-product-type", methods=("GET", "POST"))
def search_product_type():
    if "GET" == request.method:
        json_data = request.get_json()
        if not json_data or "userSearch" not in json_data:
            return jsonify({"error": "Invalid JSON format"})

        user_search = json_data["userSearch"]

        query_prod_type = """
            SELECT P.tp_id, P.nome_do_tipo, P.quantidade, D.unidade_si, D.valor
            FROM tipo_produto as P
            JOIN tipo_dimensao as D ON P.dim_id = D.dim_id
            WHERE LOWER(P.nome_do_tipo) LIKE LOWER(:user_search)
        """
        query_imgs = """
            SELECT INST.logo_url
            FROM INSTANCIA_PRODUTO as INST
            JOIN TIPO_PRODUTO as TIPO ON INST.tp_id = TIPO.tp_id
            WHERE INST.tp_id = :tipo_produto_id
        """
        db = DB.get_db()
        results = db.execute(
            text(query_prod_type), {"user_search": f"%{user_search}%"}
        ).fetchall()

        ids_prod_type = [result[0] for result in results]
        imgs_url = []
        for id in ids_prod_type:
            url = db.execute(text(query_imgs), {"tipo_produto_id": f"{id}"}).fetchone()
            if url:
                imgs_url.append(url[0])
            else:
                imgs_url.append(None)
        # Process the results as needed
        productList = [
            {
                "name": result[1],
                "imageSampleUrl": None,
                "unity": result[3],
                "qtd": result[4],
                "unities": result[2],
            }
            for result in results
        ]
        for index, img in enumerate(imgs_url):
            productList[index]["imageSampleUrl"] = img

        return jsonify({"productList": productList})

    return jsonify({"error": "Invalid request method"})


@bp.route("/recommend-markets", methods=("GET", "POST"))
def recommend_markets():
    if "GET" == request.method:
        return "Request received, response sent."


@bp.route("/search-alternative-product-instances", methods=("GET", "POST"))
def search_alternative_product_instances():
    if "GET" == request.method:
        return "Request received, response sent."
