import socks
import socket

# Tor Proxy Configuration
SOCKS_PORT = 9050


def setup_tor_proxy():
    """Setup SOCKS5 proxy for Tor"""
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", SOCKS_PORT)
    socket.socket = socks.socksocket


SCRAPABLE_SITES = {
    "Ahmia": {"url": "https://ahmia.fi/", "search": "https://ahmia.fi/search?q="},
    "OnionLand": {"url": "http://onionlandsearchengine.com", "search": "http://onionlandsearchengine.com/search?q="},
    "Dark.Fail": {"url": "https://dark.fail/", "search": "https://dark.fail/"},
    "Dread Forum": {"url": "http://dreadditevelidot.onion", "search": "http://dreadditevelidot.onion"},
    "DeepPaste": {"url": "http://deeppaste.onion", "search": "http://deeppaste.onion"},
    "NVD": {"url": "https://nvd.nist.gov/", "search": "https://nvd.nist.gov/vuln/search/results?query="},
    "ExploitDB": {"url": "https://www.exploit-db.com/", "search": "https://www.exploit-db.com/search?q="},
    "Cybercrime Tracker": {"url": "https://cybercrime-tracker.net/", "search": "https://cybercrime-tracker.net/"},
    "Mitre ATT&CK": {"url": "https://attack.mitre.org/groups/", "search": "https://attack.mitre.org/groups/"},
}

THREAT_KEYWORDS = ["exploit", "ransomware", "leak", "darknet", "hack", "breach", "malware", "data dump", "credential"]

TOR_PROXY = "socks5h://127.0.0.1:9050"
