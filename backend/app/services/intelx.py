import requests
import logging

# IntelX API Configuration
INTELX_API_KEY = "your-api-key-here"
INTELX_API_URL = "https://2.intelx.io"
HEADERS = {
    "x-key": INTELX_API_KEY,
    "User-Agent": "IX-Python/1.0",
}


def search_intelx(query, max_results=10):
    """
    Searches IntelX for dark web threats.

    Args:
        query (str): Search term.
        max_results (int): Max results to retrieve.

    Returns:
        list: Formatted search results.
    """
    search_payload = {
        "term": query,
        "maxresults": max_results,
        "media": 0,  # Search all media types
        "sort": 2,  # Sort by relevance
        "terminate": [],
    }

    try:
        # Step 1: Initiate Search
        response = requests.post(f"{INTELX_API_URL}/intelligent/search", headers=HEADERS, json=search_payload)
        response.raise_for_status()
        search_id = response.json().get("id")

        if not search_id:
            logging.error("IntelX search ID not found.")
            return []

        # Step 2: Retrieve Search Results
        result_response = requests.get(
            f"{INTELX_API_URL}/intelligent/search/result?id={search_id}&limit={max_results}", headers=HEADERS
        )
        result_response.raise_for_status()
        result_data = result_response.json()

        return parse_intelx_results(result_data)

    except requests.RequestException as e:
        logging.error(f"IntelX API Request Failed: {e}")
        return []


def parse_intelx_results(data):
    """
    Parses IntelX search results and extracts relevant fields.

    Args:
        data (dict): Raw search result data.

    Returns:
        list: Formatted results.
    """
    if not data or "records" not in data:
        return []

    parsed_results = []
    for record in data["records"]:
        parsed_results.append(
            {
                "title": record.get("name", "Unknown"),
                "date": record.get("date", "N/A"),
                "category": record.get("bucket", "Unknown"),
                "onion_links": [f"https://intelx.io/?did={record.get('systemid')}"] if record.get("systemid") else [],
                "preview": record.get("preview", "No preview available"),
            }
        )

    return parsed_results
