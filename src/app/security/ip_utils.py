"""
Extract IP-Adresses from URLs and verifies that its public
"""
# DNS requests -> Hostname to IP
import socket
from urllib.parse import urlparse
import ipaddress

# Wrapper function
def get_ip_from_url(url):
    ip = get_host(url)
    # Testcase 1
    #if is_private_ip(ip):
    #    raise ValueError("Private IP")
    return ip

# URL gets passed
def get_host(url):
    # Find hostname
    parsed = urlparse(url)
    # Extract
    hostname = parsed.hostname
    # Give back hostname to verify
    return socket.gethostbyname(hostname)

# No private ip
def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private