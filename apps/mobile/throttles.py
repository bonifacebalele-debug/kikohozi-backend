from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """Limits anonymous login attempts per client IP to slow credential stuffing."""

    scope = "login"
