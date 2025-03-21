import requests

ONION_SEARCH_ENGINES = {
    "Ahmia": "https://ahmia.fi/search/",
    "OnionLand": "http://onionlandsearchengine.com/search?q=",
    "Phobos": "http://phobos.engine/?q=",
}


def search_ahmia(query):
    """Search dark web using Ahmia."""
    response = requests.get(f"{ONION_SEARCH_ENGINES['Ahmia']}?q={query}")
    return response.json() if response.status_code == 200 else None


def search_onionland(query):
    """Search dark web using OnionLand."""
    response = requests.get(f"{ONION_SEARCH_ENGINES['OnionLand']}{query}")
    return response.text if response.status_code == 200 else None


def search_phobos(query):
    """Search dark web using Phobos."""
    response = requests.get(f"{ONION_SEARCH_ENGINES['Phobos']}{query}")
    return response.text if response.status_code == 200 else None
