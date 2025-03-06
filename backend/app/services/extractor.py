import re


# === 🛠 Extraction Functions for Each Site ===
def extract_onion_links(soup):
    return [
        {"type": "onion_link", "value": link["href"]}
        for link in soup.find_all("a", href=True)
        if "onion" in link["href"]
    ]


def extract_shodan_ips(soup):
    return [
        {"type": "exposed_ip", "value": ip.text.strip()}
        for ip in soup.find_all("a", href=re.compile(r"^/host/\d+\.\d+\.\d+\.\d+$"))
    ]


def extract_data_breaches(soup):
    return [{"type": "data_breach", "value": breach.text.strip()} for breach in soup.find_all("h3")]


def extract_malware_domains(soup):
    return [
        {"type": "malware_domain", "value": cols[1].text.strip()}
        for row in soup.find_all("tr")
        if (cols := row.find_all("td")) and len(cols) > 1
    ]


def extract_threat_actors(soup):
    return [
        {"type": "threat_actor", "value": actor.text.strip()}
        for actor in soup.find_all("a", href=re.compile(r"/groups/G\d+"))
    ]


def extract_iocs(soup):
    return [{"type": "ioc", "value": ioc.text.strip()} for ioc in soup.find_all("td")]


# Mapping Sites to Functions
EXTRACTION_FUNCTIONS = {
    "Ahmia": extract_onion_links,
    "OnionLand": extract_onion_links,
    "Shodan": extract_shodan_ips,
    "Have I Been Pwned": extract_data_breaches,
    "Cybercrime Tracker": extract_malware_domains,
    "Mitre ATT&CK Threat Actors": extract_threat_actors,
    "ThreatFox": extract_iocs,
}


def extract_data(name, soup):
    """Extract structured data based on site type"""
    extraction_function = EXTRACTION_FUNCTIONS.get(name, lambda _: [])
    return extraction_function(soup)
