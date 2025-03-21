from fastapi import APIRouter, Query
from app.services.darkweb import fetch_intelx_data, fetch_onionsearch_data
from app.services.onion_search import search_ahmia, search_onionland
from app.utils.formatting import normalize_darkweb_data

router = APIRouter()


@router.get("/darkweb")
def get_darkweb_data(keyword: str = Query(..., description="Keyword to search on the Dark Web")):
    """Fetch dark web intelligence from various sources"""

    results = [
        normalize_darkweb_data("IntelX", fetch_intelx_data(keyword), "Dark Web Leak"),
        normalize_darkweb_data("OnionSearch", fetch_onionsearch_data(keyword), "Hidden Services"),
        normalize_darkweb_data("Ahmia", search_ahmia(keyword), "Hidden Services"),
        normalize_darkweb_data("OnionLand", search_onionland(keyword), "Hidden Services"),
    ]

    return {"query": keyword, "results": [r for r in results if r]}
