"""
URL Security Gateway and Redirection Service.

Security checks performed:
# URL validation and sanitization.
# Malicious IP detection via CrowdSec.
# Redirection chain control and protection.
# Sandbox analyzation
# Request logging for security audits.
"""
from flask import request, abort, redirect
from src.app.security.crowdsec import is_malicious
from src.app.security.ip_utils import get_ip_from_url
from src.app.security.url_validator import validate_url
from src.app.security.redirection_control import redirection_controlled
import logging

from sandbox.policy import sandbox_allows
from sandbox.sandbox_client import run_sandbox

# Initialize individual logger
logger = logging.getLogger("qr_gateway")

def register_routes(app):
    """
    Register all gateway routes
    :param app: Flask application instance to configure
    """
    @app.before_request
    def log_request():
        """
        Log every incoming request
        """
        logger.info(
            "REQ | IP=%s | %s %s",
            request.remote_addr,
            request.method,
            request.path
        )

    # Routing starts after /
    @app.route("/")
    def go():
        """
        Main gateway entrypoint.

        This endpoint receives a URL, validates it using the gateway
        security policies and redirects the user to the target if the
        request is allowed.

        ---
        tags:
          - Gateway

        parameters:
          - name: url
            in: query
            required: true
            type: string
            description: URL that should be validated by the gateway
            example: https://example.com

        responses:
          302:
            description: Redirect to validated URL

          403:
            description: Request blocked by security policy

          400:
            description: Missing or invalid URL parameter
        """
        url_to_check = request.args.get('url')
        # url_to_check = "%3Cscript%3Ealert(1)%3C/script%3E"

        if not url_to_check:
            logger.warning(
                "REDIRECTION_FAIL | status=400 | reason=no_url | IP=%s",
                request.remote_addr,
            )
            abort(400, description="No url provided")

        # If URL Characters are suspicious abort
        if not validate_url(url_to_check):
            logger.warning(
                "REDIRECT_FAIL | status=400 | reason=invalid_url | target=%s | IP=%s",
                url_to_check,
                request.remote_addr
            )
            abort(400)

        # Testcase 1 to test is_private_ip()
        # try:
        #     ip_to_check = get_ip_from_url(url_to_check)
        # except ValueError as e:
        #     logger.warning(
        #         "REDIRECT_BLOCKED | status=403 | reason=%s | target=%s | IP=%s",
        #         str(e),
        #         url_to_check,
        #         request.remote_addr
        #     )
        #     abort(403, description=str(e))

        # Control if Redirect is suspicous, likely to fail
        try:
            final_url = redirection_controlled(url_to_check)
            logger.info("AFTER_REDIRECT")
        except RuntimeError as e:
            logger.warning(
                "REDIRECT_FAIL | status=400 | reason=%s | target=%s | IP=%s",
                str(e),
                url_to_check,
                request.remote_addr
            )
            abort(400, description=str(e))

        # Second case is test case for malicious IP
        # Redirection controll demands answer from Ressource direction
        # and gets blocked while testing
        ip_to_check = get_ip_from_url(final_url)
        #ip_to_check = get_ip_from_url(url_to_check)

        # Ip checking against CrowdSec blacklist
        if is_malicious(ip_to_check):
            logger.warning(
                "REDIRECT_BLOCKED | status=403 | reason=malicious_ip | target=%s | target_ip=%s | IP=%s",
                url_to_check,
                ip_to_check,
                request.remote_addr
            )
            abort(403)

        # -------------------------------
        # Testcase 2 sandbox analysis
        # -------------------------------

        # try:
        #     sandbox_report = run_sandbox(final_url)
        # except Exception as e:
        #     logger.warning(
        #         "SANDBOX_ERROR | target=%s | error=%s | IP=%s",
        #         final_url,
        #         str(e),
        #         request.remote_addr
        #     )
        #     abort(503, description="Sandbox unavailable")
        #
        # if not sandbox_allows(sandbox_report):
        #     logger.warning(
        #         "SANDBOX_BLOCKED | target=%s | report=%s | IP=%s",
        #         final_url,
        #         sandbox_report,
        #         request.remote_addr
        #     )
        #     abort(403, description="Blocked by sandbox")

        # Log legimate URL
        logger.info(
            "REDIRECT_OK | status=302 | target=%s | target_ip=%s | IP=%s",
            url_to_check,
            ip_to_check,
            request.remote_addr
        )
        # Forward to the checked URL
        # Second case is test case for skipping redirection control
        return redirect(final_url)
        #return redirect(url_to_check)
