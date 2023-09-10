import json
import os
import pickle
import re
import string
from typing import List

import requests
import unidecode
from bs4 import BeautifulSoup

from dtypes import Market, Product

BASIC_URL = "https://www.ifood.com.br/delivery"
## TODO: implement the exceptions handler


def load_products_from_website(market: Market, save_locally: bool = False) -> List[Product]:
    """Get the products list from a market
    Args:
        market: the market object
        save_locally: if should save a copy of the data locally
    Returns:
        List, a list of the products from the given market
    """
    products = []

    # Get the site response
    headers = _get_headers(market)
    session = requests.Session()
    market_url = _build_market_url(market)
    session.get(market_url)
    response = session.get(f"https://wsloja.ifood.com.br/ifood-ws-v3/v1/merchants/{market.id}/catalog", headers=headers)

    # Parse response
    response_json = json.loads(response.text)
    menu = response_json["data"]["menu"]

    # Build the Product object
    # The menu splits the products by category
    for category_menu in menu:
        category = category_menu["name"]
        itens = category_menu["itens"]
        for item in itens:
            product = Product()
            product.category = category
            product.description = item.get("description")
            product.details = item.get("details")
            product.logoUrl = item.get("logoUrl")
            product.needChoices = item.get("needChoices")
            product.unitPrice = item.get("unitPrice")
            product.unitMinPrice = item.get("unitMinPrice")
            product.productTags = item.get("productTags")
            product.additionalInfo = item.get("additionalInfo")
            products.append(product)

    # Save the data in a local file
    products_file = _get_market_local_file(market)
    if save_locally:
        with open(products_file, "wb") as file:
            pickle.dump(products, file, protocol=pickle.HIGHEST_PROTOCOL)

    return products


def load_products_from_local_file(market: Market) -> List[Product]:
    """Get the products list from a current file

    Args:
        market: the market object

    Returns:
        List, a list of the products from the given market
    """
    products_file = _get_market_local_file(market)
    if os.path.exists(products_file):
        with open(products_file, "rb") as handle:
            return pickle.load(handle)
    return None


def list_markets_in_city(city: str, state_acronym: str) -> List[Market]:
    """List all markets in the city
    Args:
    city: The city name E.g. "São José dos campos", "Brasília"
    state_acronym: The state abreviation E.g. "SP", "sp", "RJ"

    Returns:
        List, a list of the markets in the city
    """
    # Check if the state acronym is in correct format
    assert len(state_acronym) == 2
    markets = []

    city = _normalize_name(city)
    city = city.replace(" ", "-")
    # Parsing to the url format
    city_slug = f"{city}-{state_acronym.lower()}"
    # Make the request
    response = requests.get(f"{BASIC_URL}/{city_slug}")

    # Parse response
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find("script", {"type": "application/json"}).text
    data = json.loads(text)
    companies = data["props"]["initialState"]["restaurantsByCity"]["list"]

    for company in companies:
        if company["mainFoodType"]["name"] == "Mercado":
            market = Market()
            market.city = city_slug
            market.slug_name = company["slug"]
            market.id = company["id"]
            market.name = company["name"]
            market.closed = company["closed"]
            markets.append(market)
    return markets


def _build_market_url(market: Market):
    """Build the url from market main page"""
    return f"{BASIC_URL}/{market.city}/{market.slug_name}/{market.id}"


def _normalize_name(name: str) -> str:
    """Normalize a string for the default pattern

    Args:
        name: the string to be normalized
    Returns:
        str, the normalized name
    """
    # Remove the punctuation from the string, replacing by a space (Multiple spaces are removed further)
    name = unidecode.unidecode(name).translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    # Remove repeated spaces
    name = re.sub(" +", " ", name)
    name = name.lower().strip()
    return name


def _get_market_local_file(market: Market):
    return f"{market.slug_name}.pickle"


def _get_headers(market):
    """Get the required headers to access ifood database"""
    return {
        "Access_key": "########",
        "authority": "wsloja.ifood.com.br",
        "method": "GET",
        "path": f"/ifood-ws-v3/v1/merchants/{market.id}/catalog?category_items_size=12",
        "scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=1",
        "App_version": "9.97.0",
        "Browser": "Linux",
        "Cache-Control": "no-cache, no-store",
        "Origin": "https://www.ifood.com.br",
        "Platform": "Desktop",
        "Referer": "https://www.ifood.com.br/",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Secret_key": "########",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "X-Device-Model": "Linux Chrome",
        "X-Ifood-Device-Id": "########",
        "X-Ifood-Session-Id": "########",
    }


def generate_data_file(data: List[Product], filename: str) -> None:
    """Generate a txt file with the data, writing in list format

    Args:
        data: a list of products with the data to be saved in the file
        filename: the file to save the data
    """
    with open(filename, "w+") as f:
        f.write("[")
        for product in data:
            name = product.description.replace('"', "")
            p = {
                "product": name,
                "tags": [],
            }
            f.write(f"{repr(p)},\n")
        f.write("]\n")
