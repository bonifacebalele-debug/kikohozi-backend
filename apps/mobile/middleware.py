import uuid
import time
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Attaches a UUID to every request and logs timing on completion."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())[:8]
        start = time.monotonic()

        response = self.get_response(request)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        response["X-Request-ID"] = request.request_id

        logger.debug(
            "%s %s %s %dms",
            request.method,
            request.path,
            response.status_code,
            elapsed_ms,
            extra={"request_id": request.request_id},
        )

        return response
