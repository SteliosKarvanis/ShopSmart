from math import radians, sin, cos, sqrt, atan2


def convert_money_string_to_float(money_str):
    """
    Converts money string to float

    Parameters:
        money_str (str): Input money string in the format R$ D,CT,
                         where D is a natural number and C,T are digits.

    Returns:
        float: Converted float value (D.CT).
    """
    amount_str = money_str.replace("R$ ", "")
    amount_str = amount_str.replace(",", ".")
    amount_float = float(amount_str)

    return amount_float


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate haversine distance between two geographic coordinates and return their distance in kilometers.

    Parameters:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: Haversine distance between the two points in kilometers.
    """
    R = 6371e3
    phi_1 = radians(lat1)
    phi_2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2) * sin(delta_phi / 2) + cos(phi_1) * cos(phi_2) * sin(
        delta_lambda / 2
    ) * sin(delta_lambda / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c / 1000  # in kilometers
    return distance


def count_items(cart):
    """
    Count the number of items in the cart

    Parameters:
        cart (dict): Dictionary associating items with boolean values.

    Returns:
        int: Number of items in the cart.
    """
    return sum(value is True for value in cart.values())
