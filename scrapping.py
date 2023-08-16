from bs4 import BeautifulSoup
import requests
import json

BASIC_URL = "https://www.ifood.com.br/delivery"

class Market:
    city:str
    slug_name:str
    id:str
    name:str
    closed:bool

    def __repr__(self) -> str:
        return f"""
        city: {self.city},
        slug_name: {self.slug_name},
        id: {self.id},
        name: {self.name},
        closed: {self.closed}"""


def get_products_from_market(market: Market):
    headers = _get_headers(market)
    session = requests.Session()
    market_url = _build_market_url(market)
    session.get(market_url)
    response = session.get(f"https://wsloja.ifood.com.br/ifood-ws-v3/v1/merchants/{market.id}/catalog?category_items_size=12", headers=headers)
    return response

def list_markets_in_city(city: str, state_acronym: str):
    city_slug = f"{city.lower()}-{state_acronym.lower()}"
    markets = []
    response = requests.get(f"{BASIC_URL}/{city_slug}")
    soup = BeautifulSoup(response.text, 'html.parser')
    json_str = soup.find_all("script", {"type": "application/json"})[0].text
    dic = json.loads(json_str)
    restaurants_list = dic['props']['initialState']['restaurantsByCity']['list']
    for company in restaurants_list:
        if company['mainFoodType']['name'] == "Mercado":
            market = Market()
            market.city = city_slug
            market.slug_name = company["slug"]
            market.id = company["id"]
            market.name = company['name']
            market.closed = company['closed']
            markets.append(market)
    return markets


def _build_market_url(market: Market):
    return f"{BASIC_URL}/{market.city}/{market.slug_name}/{market.id}"

def _get_headers(market):
    return {
        "Access_key":"69f181d5-0046-4221-b7b2-deef62bd60d5",
        "authority":"wsloja.ifood.com.br",
        "method":"GET",
        "path":f"/ifood-ws-v3/v1/merchants/{market.id}/catalog?category_items_size=12",
        "scheme":"https",
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"pt-BR,pt;q=1",
        "App_version":"9.97.0",
        "Browser":"Linux",
        "Cache-Control":"no-cache, no-store",
        "Origin":"https://www.ifood.com.br",
        "Platform":"Desktop",
        "Referer":"https://www.ifood.com.br/",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"Linux",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-site",
        "Secret_key":"9ef4fb4f-7a1d-4e0d-a9b1-9b82873297d8",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "X-Device-Model":"Linux Chrome",
        "X-Ifood-Device-Id":"3019aba7-bae2-49c4-bf2d-2baa03055acd",
        "X-Ifood-Session-Id":"4b8d544f-c05a-4fdb-9d36-3e7be28cd5d3",
        }
