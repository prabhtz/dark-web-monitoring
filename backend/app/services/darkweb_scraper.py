import requests
import random
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from app.config import TOR_PROXY
from app.utils.formatting import clean_text
from app.utils.formatting import normalize_darkweb_data

# ✅ Supported Onion Search Engines
ONION_SEARCH_ENGINES = {
    "Ahmia": "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion",
    "Phobos": "http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion",
    "OnionLand": "http://3bbad7fauom4d6sg.onion",
    "OnionSearchServer": "http://3fzh7yuupdfyjhwt.onion",
    "Tor66": "http://tor66sewebgixwhcqf.onion",
    "Haystack": "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion",
    "Torgle": "http://no6m4wzdexe3auiupv2z.onion",
}

# ✅ User agents to mimic real browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
]


def get_tor_session():
    """Creates a Tor session using SOCKS5 proxy."""
    session = requests.Session()
    session.proxies = {"http": TOR_PROXY, "https": TOR_PROXY}
    return session


def search_darkweb(keyword: str):
    """Search multiple onion search engines for the given keyword."""
    session = get_tor_session()
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    raw_results = []

    for engine, url in ONION_SEARCH_ENGINES.items():
        try:
            search_url = f"{url}/search?q={urlparse.quote(keyword)}"
            response = session.get(search_url, headers=headers, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                search_results = extract_onion_links(engine, soup)

                if search_results:
                    raw_results.extend(search_results)

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error querying {engine}: {e}")

    # Normalize and apply risk scoring
    return normalize_darkweb_data("Dark Web Aggregator", raw_results, "Hidden Services")


def extract_onion_links(engine: str, soup: BeautifulSoup):
    """Extract valid onion links from different search engine results."""
    results = []

    if engine == "Ahmia":
        for item in soup.select("li.result h4 a"):
            link = item["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(item.text), "onion_links": [link]})

    elif engine == "Phobos":
        for result in soup.select(".serp .titles a"):
            link = result["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(result.text), "onion_links": [link]})

    elif engine == "Tor66":
        for i in soup.find("hr").find_all_next("b"):
            if i.find("a"):
                link = i.find("a")["href"]
                if ".onion" in link:
                    results.append({"source": engine, "title": clean_text(i.find("a").text), "onion_links": [link]})

    elif engine == "OnionLand":
        for result in soup.select("div.result-title a"):
            link = result["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(result.text), "onion_links": [link]})

    elif engine == "OnionSearchServer":
        for result in soup.select("div.result-item a"):
            link = result["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(result.text), "onion_links": [link]})

    elif engine == "Haystack":
        for result in soup.select("div.title a"):
            link = result["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(result.text), "onion_links": [link]})

    elif engine == "Torgle":
        for result in soup.select("a.result-title"):
            link = result["href"]
            if ".onion" in link:
                results.append({"source": engine, "title": clean_text(result.text), "onion_links": [link]})

    return results
