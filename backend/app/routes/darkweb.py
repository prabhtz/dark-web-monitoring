from fastapi import APIRouter, Query
from app.services.darkweb import search_darkweb
from app.utils.formatting import normalize_darkweb_data

router = APIRouter()


@router.get("/darkweb")
def get_darkweb_data(keyword: str = Query(..., description="Keyword to search on the dark web")):
    """
    Fetch dark web intelligence from multiple sources.
    - Searches IntelX & onion search engines.
    - Returns formatted results including onion links.
    """
    darkweb_results = search_darkweb(keyword)

    return {
        "query": keyword,
        "results": [
            normalize_darkweb_data(source, result, "Hidden Services") for source, result in darkweb_results.items()
        ],
    }
