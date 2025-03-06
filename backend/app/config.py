import socks
import socket

# Tor Proxy Configuration
SOCKS_PORT = 9050


def setup_tor_proxy():
    """Setup SOCKS5 proxy for Tor"""
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", SOCKS_PORT)
    socket.socket = socks.socksocket


# URLs of sites to scrape
SCRAPABLE_SITES = {
    "Ahmia": "https://ahmia.fi/",
    "OnionLand": "http://onionlandsearchengine.com",
    "Shodan": "https://www.shodan.io/",
    "Have I Been Pwned": "https://haveibeenpwned.com/",
    "Cybercrime Tracker": "https://cybercrime-tracker.net/",
    "Mitre ATT&CK Threat Actors": "https://attack.mitre.org/groups/",
    "ThreatFox": "https://threatfox.abuse.ch/",
}
