from oauth2app.oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from oauth2app.oauth2app.models import AccessRange


def username(request):
    """Return username of user associated with access token."""
    scope = AccessRange.objects.get(key="date_joined")
    authenticator = JSONAuthenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response(
        {
            "date_joined": authenticator.user.username
        }
    )
