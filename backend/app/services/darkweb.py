import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API keys

# API Endpoints
DARK_WEB_API_URLS = {
    "OnionSearch": "https://onionsearchengine.com/api/search",
}


# IntelX API Key from .env
INTELX_API_KEY = os.getenv("INTELX_API_KEY")
INTELX_API_URL = "https://free.intelx.io/"


def fetch_intelx_data(query):
    """Fetch Dark Web intelligence from IntelX API and extract Onion links"""
    print(f"Fetching IntelX data for {query}...")

    try:
        # Step 1: Perform Search Query
        search_payload = {"term": query, "maxresults": 10, "media": 0, "sort": 2, "terminate": []}
        search_headers = {"x-key": INTELX_API_KEY}
        search_response = requests.post(
            f"{INTELX_API_URL}intelligent/search", json=search_payload, headers=search_headers
        )

        if search_response.status_code != 200:
            print(f"IntelX Search Error: {search_response.status_code} - {search_response.text}")
            return None

        search_results = search_response.json()
        search_id = search_results.get("id")
        if not search_id:
            print(f"No search ID returned from IntelX.")
            return None

        # Step 2: Fetch Search Results
        results_url = f"{INTELX_API_URL}intelligent/search/result?id={search_id}&limit=10&statistics=1&previewlines=8"
        result_response = requests.get(results_url, headers=search_headers)

        if result_response.status_code != 200:
            print(f"IntelX Result Error: {result_response.status_code} - {result_response.text}")
            return None

        results = result_response.json()
        if not results.get("records"):
            print("No results found on IntelX.")
            return None

        # Step 3: Extract Onion Links & Format Data
        parsed_results = []

        for record in results["records"]:
            storage_id = record.get("storageid")
            preview_url = f"{INTELX_API_URL}file/preview?sid={storage_id}&f=0&l=8&c=1&m=1&b=pastes&k={INTELX_API_KEY}"
            preview_response = requests.get(preview_url, headers=search_headers)

            preview_text = preview_response.text if preview_response.status_code == 200 else "Preview unavailable"

            # Extract `.onion` links from selectors
            selectors = record.get("selectors", [])
            extracted_onion_links = [sel for sel in selectors if sel.endswith(".onion")]

            parsed_results.append(
                {
                    "title": record.get("name", "Unknown"),
                    "date": record.get("date"),
                    "preview": preview_text,
                    "intelx_link": f"https://intelx.io/?did={record.get('systemid')}",
                    "onion_links": extracted_onion_links,
                }
            )

        return parsed_results

    except Exception as e:
        print(f"IntelX API Error: {e}")
        return None


def fetch_onionsearch_data(query):
    """Fetch Hidden Services results from OnionSearch"""
    print(f"Searching OnionSearch for {query}...")

    url = f"https://onionsearchengine.com/search?q={query}&submit=Search"

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
