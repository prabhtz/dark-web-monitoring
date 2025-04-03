import requests
import logging
from bs4 import BeautifulSoup

# Onion search engines
AHMIA_URL = "https://ahmia.fi/search/"
ONIONLAND_URL = "http://onionlandsearchengine.com/search/"


def search_ahmia(query):
    """
    Searches Ahmia (Dark Web Search Engine).

    Args:
        query (str): Search term.

    Returns:
        list: Search results.
    """
    try:
        response = requests.get(f"{AHMIA_URL}?q={query}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.select("li.result h4 a"):
            results.append({"title": result.text, "url": result["href"]})

        return results
    except requests.RequestException as e:
        logging.error(f"Ahmia search failed: {e}")
        return []


def search_onionland(query):
    """
    Searches OnionLand search engine.

    Args:
        query (str): Search term.

    Returns:
        list: Search results.
    """
    try:
        response = requests.get(f"{ONIONLAND_URL}?q={query}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.select("h2.title a"):
            results.append({"title": result.text, "url": result["href"]})

        return results
    except requests.RequestException as e:
        logging.error(f"OnionLand search failed: {e}")
        return []
