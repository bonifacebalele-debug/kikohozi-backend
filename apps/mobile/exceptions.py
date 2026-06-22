import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def mobile_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get("request")
    request_id = getattr(request, "request_id", "-")

    if response is not None:
        logger.warning(
            "API error",
            extra={"request_id": request_id},
            exc_info=exc,
        )
        return Response(
            {
                "success": False,
                "message": _extract_message(response.data),
                "errors": response.data if isinstance(response.data, dict) else {},
            },
            status=response.status_code,
        )

    logger.error(
        "Unhandled exception",
        extra={"request_id": request_id},
        exc_info=exc,
    )
    return Response(
        {
            "success": False,
            "message": "An unexpected server error occurred.",
            "errors": {},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _extract_message(data):
    if isinstance(data, dict):
        return data.get("detail", "Validation failed.")
    if isinstance(data, list) and data:
        return str(data[0])
    return "An error occurred."
