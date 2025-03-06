import socks
import socket

# Tor Proxy Configuration
SOCKS_PORT = 9050


def setup_tor_proxy():
    """Setup SOCKS5 proxy for Tor"""
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", SOCKS_PORT)
    socket.socket = socks.socksocket


SCRAPABLE_SITES = {
    "Ahmia": {"url": "https://ahmia.fi/", "search": "https://ahmia.fi/search/?q="},
    "OnionLand": {"url": "http://onionlandsearchengine.com", "search": "http://onionlandsearchengine.com/search?q="},
    "Dark.Fail": {"url": "https://dark.fail/", "search": None},  # No search function
    "Dread Forum": {"url": "http://dreadditevelidot.onion", "search": None},  # Requires login
    "DeepPaste": {"url": "http://deeppaste.onion", "search": None},  # No search function
    "Recon": {"url": "https://recon.dev/", "search": "https://recon.dev/search?q="},
    "NVD": {"url": "https://nvd.nist.gov/", "search": "https://nvd.nist.gov/vuln/search/results?query="},
    "ExploitDB": {"url": "https://www.exploit-db.com/", "search": "https://www.exploit-db.com/search?q="},
    "Cybercrime Tracker": {"url": "https://cybercrime-tracker.net/", "search": None},  # No search function
    "Mitre ATT&CK": {"url": "https://attack.mitre.org/groups/", "search": None},  # No search function
    "Shodan": {"url": "https://www.shodan.io/", "search": "https://www.shodan.io/search?query="},
    "GreyNoise": {"url": "https://www.greynoise.io/", "search": "https://www.greynoise.io/viz/query?gnql="},
    "ThreatFox": {"url": "https://threatfox.abuse.ch/", "search": "https://threatfox.abuse.ch/browse.php?search="},
}

THREAT_KEYWORDS = ["exploit", "ransomware", "leak", "darknet", "hack", "breach", "malware", "data dump", "credential"]

TOR_PROXY = "socks5h://127.0.0.1:9050"
