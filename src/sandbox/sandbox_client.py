"""
Communicating and requesting data from the Sandbox

Gateway is requesting the Sandbox to gather data
about the URL it wants to redirect to
"""
import requests
# Sandbox endpoint
SANDBOX_URL = "http://127.0.0.1:5001/analyze"

def run_sandbox(url: str) -> dict:
    """
    Submits URL to the sandbox for analysis and gets back results

    :param url: URL to be checked
    :return: Dictionary with results of sandbox analysis
    """
    r = requests.post(
        SANDBOX_URL,
        json={"url": url},
        timeout=20
    )
    # Automatic statuscode request to catch basic connection errors
    r.raise_for_status()
    # Returning dictionary
    return r.json()