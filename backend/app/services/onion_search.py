import requests

ONION_SEARCH_ENGINES = {
    "Ahmia": "https://ahmia.fi/search/",
    "OnionLand": "http://onionlandsearchengine.com/search?q=",
}


def search_ahmia(query):
    """Fetch Dark Web results from Ahmia"""
    print(f"Searching Ahmia for {query}...")
    url = f"https://ahmia.fi/search/?q={query}"

    try:
        response = requests.get(url, timeout=10)

        # Check for valid JSON response
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/json":
            return response.json()

        print(f"Ahmia returned non-JSON response: {response.text[:100]}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Ahmia API Error: {e}")
        return None


def search_onionland(query):
    """Fetch Hidden Services results from OnionSearch"""
    print(f"Searching OnionSearch for {query}...")

    url = f"http://onionlandsearchengine.com/search?q={query}&submit=Search"

    try:
        response = requests.get(url, timeout=10)

        # Check if response is empty or non-JSON
        if response.status_code != 200:
            print(f"OnionSearch API Error: {response.status_code}")
            return None

        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            return response.json()

        print(f"OnionSearch returned non-JSON response: {response.text[:100]}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"OnionSearch API Error: {e}")
        return None
