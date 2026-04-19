"""
URL Redirection Controller

Manually follows HTTP redirects
validates each step in a redirection chain,
preventing open redirects and more.

Should ideally catch ("Connection timeout")("Connection failed")("HTTP request failed")
in future versions
"""
from urllib.parse import urljoin
import requests
from src.app.security.url_validator import validate_url
import logging

# Logger and global variable
logger = logging.getLogger("qr_gateway")
MAX_REDIRECTS = 2

def redirection_controlled(url: str) -> str:
    """
    Safely follows redirection chain, validates each destination.

    Prevents "Open Redirect" attacks by re-validating every
    intermediate URL before proceeding to the next

    :param url: The initial URL to check.
    :return: The final destination URL after all safe redirects.
    :raises RuntimeError: If redirect limit is exceeded or a target is invalid.
    """
    current_url = url
    redirects = 0

    while True:
        # Without automatic redirect following (allow_redirects=False)
        r = requests.get(
            current_url,
            allow_redirects=False,
            timeout=5
        )

        # Check if it redirects with statuscode
        if r.status_code in (301, 302, 303, 307, 308):
            redirects += 1

            # Safety break
            if redirects > MAX_REDIRECTS:
                raise RuntimeError("Too many redirects")

            # Extract next destination from the "Location" header
            location = r.headers.get("Location")
            if not location:
                raise RuntimeError("Redirect without Location header")

            # Resolve relative paths to absolute URLs (e.g., /login -> https://site.com)
            # So it can be accessed/addressed
            next_url = urljoin(current_url, location)

            logger.info("REDIRECT_STEP | from=%s | to=%s",
                        current_url,
                        next_url)

            # Mid function security Check: Validate the new target URL before following it
            if not validate_url(next_url):
                raise RuntimeError("Redirect target not allowed")
            # current url is next
            current_url = next_url
            continue
        # The editor warns that "location" is not only str ( str | None)
        # Check above (if not location) acts as type guard,
        # ensures 'location' is a valid string before reaching urljoin
        # Return the final, successfully validated URL
        return current_url