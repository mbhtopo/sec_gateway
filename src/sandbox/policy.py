"""
Sandbox only collects Data
Logic is implemented by policy module
"""
def sandbox_allows(report: dict) -> bool:
    """
    gives back if URL is allowed or not
    :param report: Data the Sandbox gathers
    :return: true: if URL is allowed false: if URL is not allowed
    """
    # Too many redirects
    if report.get("redirects", 0) > 4:
        return False
    # Unwanted Download detected
    if report.get("downloads_detected"):
        return False
    # URL seems legit
    return True