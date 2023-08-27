from dataclasses import dataclass


@dataclass
class Market:
    city: str = ""
    slug_name: str = ""
    id: str = ""
    name: str = ""
    closed: bool = True


@dataclass
class Product:
    description: str = ""
    details: str = ""
    logoUrl: str = ""
    needChoices: str = ""
    unitPrice: str = ""
    unitMinPrice: str = ""
    productTags: str = ""
    additionalInfo: str = ""
    category: str = ""
