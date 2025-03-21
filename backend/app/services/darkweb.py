import os
import requests
from dotenv import load_dotenv
from intelx import intelx

load_dotenv()  # Load API keys

# ✅ Load API Keys
API_KEYS = {
    "IntelX": os.getenv("INTELX_API_KEY"),
}

# ✅ API Endpoints
DARK_WEB_API_URLS = {
    "DarkSearch": "https://darksearch.io/api/search",
    "OnionSearch": "https://onionsearchengine.com/api/search",
}

# ✅ IntelX Client
intelx_client = intelx(API_KEYS["IntelX"])


def fetch_intelx_data(query):
    """Fetch dark web intelligence from IntelX API (Python SDK)."""
    try:
        return intelx_client.search(query, maxresults=10)
    except Exception as e:
        return {"error": str(e)}


def fetch_darksearch_data(query):
    """Fetch search results from DarkSearch API (No Auth Required)."""
    response = requests.get(f"{DARK_WEB_API_URLS['DarkSearch']}?query={query}")
    return response.json() if response.status_code == 200 else None


def fetch_onionsearch_data(query):
    """Fetch search results from OnionSearch API (No Auth Required)."""
    response = requests.get(f"{DARK_WEB_API_URLS['OnionSearch']}?query={query}")
    return response.json() if response.status_code == 200 else None
