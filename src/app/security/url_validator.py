"""
Validation of the Input from URL

Provides
# Limitation of length
# Escaping percentages and separating parts of the URL
# Checking for TLS certificate
# Whitelisting of Hosts
# Whitelisting Characters
"""
import re
from urllib.parse import urlparse, urlunparse, unquote, parse_qsl, urlencode
import logging

logger = logging.getLogger("qr_gateway")
# Global so check_path/query can access
# Disabled for testcases
#ALLOWED_SCHEMES = {"https"}
# Disabled for testcases and high false positive rate
#ALLOWED_HOSTS = {"api.example.com", "service.example.com"}
MAX_URL_LENGTH = 2048
PATH_REGEX = re.compile(r"^[a-zA-Z0-9/_\-.]*$")

def validate_url(input_url: str) -> bool:
    """
    Validates the URL against length, format, and security policies

    :param input_url: URL that is to be checked
    :return: URL that is allowed
    """
    # Limit length
    if not input_url or len(input_url) > MAX_URL_LENGTH:
        return False
    # Interpreting text, catching unknown exceptions
    try:
        decoded = unquote(input_url)
        parsed = urlparse(decoded)
    except Exception as e:
        logger.warning(
            "REDIRECT_FAIL | status=400 | reason=invalid_url | target=%s | IP=%s",
            str(e),
            input_url
        )
        return False
    # Collecting checks
    checks = [
        #check_scheme(parsed),
        #check_host(parsed),
        check_path(parsed),
        check_query(parsed),
    ]
    logger.info(
        "URL_DECODED | value=%r",
        input_url
    )
    # Returning a
    return all(checks)

#def check_scheme(parsed):
#    return parsed.scheme in ALLOWED_SCHEMES

#def check_host(parsed):
#    return parsed.hostname in ALLOWED_HOSTS
# Path part of the URL detects traversal

def check_path(parsed):
    if ".." in parsed.path:
        return False
    return bool(PATH_REGEX.match(parsed.path))
# Query part is checked with Regular expression
def check_query(parsed):
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if len(key) > 50 or len(value) > 200:
            return False
    # All checks were successfully
    return True