from fastapi import APIRouter, Query
from app.services.darkweb import fetch_intelx_data, fetch_darksearch_data, fetch_onionsearch_data
from app.services.onion_search import search_ahmia, search_onionland, search_phobos
from app.utils.formatting import normalize_darkweb_data

router = APIRouter()


@router.get("/darkweb")
def get_darkweb_data(keyword: str = Query(...)):
    """Fetch dark web intelligence."""

    results = [
        normalize_darkweb_data("IntelX", fetch_intelx_data(keyword), "Dark Web Leak"),
        normalize_darkweb_data("DarkSearch", fetch_darksearch_data(keyword), "Dark Web Search"),
        normalize_darkweb_data("OnionSearch", fetch_onionsearch_data(keyword), "Hidden Services"),
        normalize_darkweb_data("Ahmia", search_ahmia(keyword), "Hidden Services"),
        normalize_darkweb_data("OnionLand", search_onionland(keyword), "Hidden Services"),
        normalize_darkweb_data("Phobos", search_phobos(keyword), "Hidden Services"),
    ]

    return {"query": keyword, "results": [r for r in results if r]}
