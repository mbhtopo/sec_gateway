"""
Checking if the IP of the URL is inside the Crowdsec
Blacklist for malicious IP's

Requesting Data from the CrowdSec API
Limiting Access against violation and
checking the reputation in the Json file
"""
import requests
from dotenv import load_dotenv
import os
import logging

# Initialize individual logger
logger = logging.getLogger("qr_gateway")
# Access keyfile, only for testing purposes in .env
load_dotenv("gateway.env")
# Extract key avoid hardcode key
CTI_API_KEY = os.getenv("CTI_API_KEY")

def get_api_key():
    if not CTI_API_KEY:
        raise ValueError("CTI_API_KEY not inside .env")
    return CTI_API_KEY


def is_malicious(ip):
    """
    Address reputation gets checked against malicious attribute

    :param ip: Address to be checked
    :return: true: if address is not in list false: inside Blacklist
    """
    headers = {
        "X-Api-Key": CTI_API_KEY
    }
    # cti endpoint of swagger
    url = f"https://cti.api.crowdsec.net/v2/smoke/{ip}"
    #
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Rate limit easily exceed because of request amount
        if response.status_code == 429:
            print("Rate limit exceeded")
            return True
        # Mistake on side of CrowdSec for Debugging
        if response.status_code != 200:
            print("CrowdSec not available!")
            return False
        # Storing information about IP in variable
        data = response.json()
        # Checking the attribute
        return data.get("reputation") == "malicious"
    # Safe Error handling for external API
    except Exception as e:
        logger.warning("REDIRECT_FAIL | status=400 | reason=%s | IP=%s",
                       str(e),
                       ip
                       )
        return False