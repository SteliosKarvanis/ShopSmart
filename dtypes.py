class Market:
    city: str
    slug_name: str
    id: str
    name: str
    closed: bool

    def __repr__(self) -> str:
        return (
            f"city: {self.city}, slug_name: {self.slug_name}, id: {self.id}, name: {self.name}, closed: {self.closed}"
        )


class Product:
    description: str
    details: str
    logoUrl: str
    needChoices: str
    unitPrice: str
    unitMinPrice: str
    productTags: str
    additionalInfo: str
    category: str

    # TODO: do the __repr__
