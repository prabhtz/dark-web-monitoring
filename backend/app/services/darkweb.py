import logging
from app.services.intelx import search_intelx
from app.services.onion_search import search_ahmia, search_onionland


def search_darkweb(keyword):
    """
    Searches multiple dark web intelligence sources.

    Args:
        keyword (str): Search term.

    Returns:
        dict: Results from IntelX & onion search engines.
    """
    logging.info(f"Fetching dark web intelligence for: {keyword}")

    results = {
        "IntelX": search_intelx(keyword),
        "Ahmia": search_ahmia(keyword),
        "OnionLand": search_onionland(keyword),
    }

    return results
