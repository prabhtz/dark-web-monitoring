import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    """Fetch page content from a given URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None
    except Exception as e:
        return None
