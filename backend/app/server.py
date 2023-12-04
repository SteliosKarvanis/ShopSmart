from flask import (
    Blueprint,
    request,
    jsonify,
)
from sqlalchemy import text
from . import db as DB
from . import utils as UTILS


# Create blueprint for views used in recommendation logic
bp = Blueprint("server", __name__, url_prefix="/server")


@bp.route("/search-product-type", methods=("GET", "POST"))
def search_product_type():
    """
    Endpoint for searching product types based on user input.

    Method:
        - GET: Expects a JSON payload containing the key 'userSearch' for user input.
               Returns a JSON response with a list of matching product types and associated information.

    Parameters:
        None (Uses request.json for 'GET' method).

    Returns:
        JSON:
            - For successful searches:
                {
                    "productList": [
                        {
                            "name": str,
                            "imageSampleUrl": str or None,
                            "unity": str,
                            "qtd": int,
                            "unities": int,
                            "tp_id": int
                        },
                        ...
                    ]
                }

            - For invalid JSON or missing 'userSearch':
                {"error": "Invalid JSON format"}

            - For invalid request method:
                {"error": "Invalid request method"}
    """
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

        db = DB.get_db()

        results = db.execute(
            text(query_prod_type), {"user_search": f"%{user_search}%"}
        ).fetchall()

        query_imgs = """
            SELECT INST.logo_url
            FROM instancia_produto as INST
            JOIN tipo_produto as TIPO ON INST.tp_id = TIPO.tp_id
            WHERE INST.tp_id = :tipo_produto_id
        """

        ids_prod_type = [result[0] for result in results]
        imgs_url = []
        for id in ids_prod_type:
            url = db.execute(text(query_imgs), {"tipo_produto_id": f"{id}"}).fetchone()
            if url:
                imgs_url.append(url[0])
            else:
                imgs_url.append(None)

        productList = [
            {
                "name": result[1],
                "imageSampleUrl": None,
                "unity": result[3],
                "qtd": result[4],
                "unities": result[2],
                "tp_id": result[0],
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
        json_data = request.get_json()
        if (
            not json_data
            or "userLocation" not in json_data
            or "productList" not in json_data
        ):
            return jsonify({"error": "Invalid JSON format"})

        user_location = json_data["userLocation"]
        product_list = json_data["productList"]

        query_get_markets = """
            SELECT DISTINCT nome_mercado, latitude, longitude from MERCADO
        """

        db = DB.get_db()

        result_markets = db.execute(text(query_get_markets)).fetchall()

        markets = [
            {
                "name": result[0],
                "distance-euclidean": UTILS.sqrt(
                    (result[1] - user_location["lat"]) ** 2
                    + (result[2] - user_location["lon"]) ** 2
                ),
                "distance-haversine": UTILS.calculate_distance(
                    user_location["lat"], user_location["lon"], result[1], result[2]
                ),
                "lat": result[1],
                "lon": result[2],
                "total": 0,
                "cartInstances": [],
                "cartContains": {product["tp_id"]: False for product in product_list},
            }
            for result in result_markets
        ]

        query_get_instances = """
            SELECT INST.m_id, INST.tp_id, INST.nome_produto, INST.preco, INST.disponibilidade, M.nome_mercado
            FROM instancia_produto as INST
            JOIN mercado as M ON INST.m_id = M.m_id
            WHERE tp_id = :tipo_produto_id
        """

        tp_ids = [product["tp_id"] for product in product_list]
        unities = [product["unities"] for product in product_list]

        for index, id in enumerate(tp_ids):
            instances = db.execute(
                text(query_get_instances), {"tipo_produto_id": f"{id}"}
            ).fetchall()
            for instance in instances:
                for market in markets:
                    if market["name"] == instance[5]:
                        if instance[4]:
                            subtotal = int(
                                str(unities[index])
                            ) * UTILS.convert_money_string_to_float(instance[3])
                            market["cartInstances"].append(
                                {
                                    "name": instance[2],
                                    "qte": unities[index],
                                    "unityPrice": instance[3],
                                    "subtotal": subtotal,
                                }
                            )
                            market["total"] += subtotal
                            market["cartContains"][tp_ids[index]] = True

        return jsonify({"Markets": markets})
    return jsonify({"error": "Invalid request method"})


@bp.route("/search-alternative-product-instances", methods=("GET", "POST"))
def search_alternative_product_instances():
    if "GET" == request.method:
        return "Request received, response sent."
