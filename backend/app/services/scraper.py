import requests
from bs4 import BeautifulSoup
from app.config import SCRAPABLE_SITES, DEFAULT_THREAT_KEYWORDS, TOR_PROXY


def fetch_page(url):
    """Fetch page content using Tor proxy for .onion sites, direct for others."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": TOR_PROXY, "https": TOR_PROXY} if ".onion" in url else {}

        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None


def extract_threat_links(soup, site_name, keywords):
    """Extract URLs from search results that match threat keywords."""
    links = []
    base_url = SCRAPABLE_SITES[site_name]["url"]

    for link in soup.find_all("a", href=True):
        url = link["href"]
        text = link.get_text().lower()

        if any(keyword in url.lower() or keyword in text for keyword in keywords):
            if url.startswith("/"):  # Convert relative URLs to absolute
                url = f"{base_url.rstrip('/')}{url}"
            links.append({"site": site_name, "url": url, "context": text})

    return links


def scrape_sites(keywords=None):
    """Scrape sources for the given keywords using main pages & search queries."""
    keywords = keywords or DEFAULT_THREAT_KEYWORDS
    results = []

    for site, info in SCRAPABLE_SITES.items():
        if info["search"] is None:
            print(f"Scraping main page of {site} for keywords: {keywords} ...")
            soup = fetch_page(info["url"])
            if soup:
                results.extend(extract_threat_links(soup, site, keywords))

        else:
            for keyword in keywords:
                search_url = f"{info['search']}{keyword.replace(' ', '+')}"
                print(f"Scraping {site} search results for '{keyword}' at {search_url} ...")
                soup = fetch_page(search_url)
                if soup:
                    results.extend(extract_threat_links(soup, site, keywords))

    return results
