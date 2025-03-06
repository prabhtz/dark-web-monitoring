import requests
from bs4 import BeautifulSoup
from app.config import SCRAPABLE_SITES, THREAT_KEYWORDS, TOR_PROXY


def fetch_page(url):
    """Fetch page content using the appropriate proxy (Tor for .onion sites)."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": TOR_PROXY, "https": TOR_PROXY} if ".onion" in url else {}

        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None


def extract_threat_links(soup, site_name):
    """Extract valid URLs related to threats based on keywords."""
    links = []
    base_url = SCRAPABLE_SITES[site_name]["url"]

    for link in soup.find_all("a", href=True):
        url = link["href"]
        text = link.get_text().lower()

        if any(keyword in url.lower() or keyword in text for keyword in THREAT_KEYWORDS):
            if url.startswith("/"):  # Convert relative URLs to absolute
                url = f"{base_url.rstrip('/')}{url}"
            search_url = (
                f"{SCRAPABLE_SITES[site_name]['search']}{text.replace(' ', '+')}"
                if "search" in SCRAPABLE_SITES[site_name]
                else base_url
            )
            links.append({"site": site_name, "url": url, "context": text, "source_page": search_url})
    return links


def scrape_sites():
    """Scrape the best Surface & Dark Web sources and return relevant threat-related URLs."""
    results = []
    for site, info in SCRAPABLE_SITES.items():
        print(f"Scraping {site}...")
        soup = fetch_page(info["url"])
        if soup:
            results.extend(extract_threat_links(soup, site))
    return results
