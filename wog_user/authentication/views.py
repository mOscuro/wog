from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.views import LoginView
from rest_framework.compat import is_anonymous
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
import rest_auth

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user or is_anonymous(request.user)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class LoginView(rest_auth.views.LoginView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.

    Error Code:

    * 400 Bad Request with error details (field + message)
    """
    permission_classes = (IsAnonymous,)
    authentication_classes = (TokenAuthentication,)


class LogoutView(rest_auth.views.LogoutView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (IsAuthenticated,)


class UserDetailsView(rest_auth.views.UserDetailsView):
    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:

    * Required: token
    * Optional: first_name, last_name and UserProfile fields

    Returns the updated UserProfile and/or User object.
    """


class PasswordResetView(rest_auth.views.PasswordResetView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """


class PasswordResetConfirmView(rest_auth.views.PasswordResetConfirmView):
    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """


class PasswordChangeView(rest_auth.views.PasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
