from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session auth without CSRF enforcement.
    Mobile apps cannot supply CSRF tokens, so we skip that check.
    Protection against CSRF still exists at the transport layer (HTTPS + SameSite cookie).
    """

    def enforce_csrf(self, request):
        pass
