

from django.conf import settings
from django.contrib.auth import login, logout
from knox.models import AuthToken
from rest_framework import mixins, status
from rest_framework.compat import is_anonymous
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from wog_user.authentication.serializers import (LoginSerializer,
                                                PasswordResetConfirmSerializer,
                                                PasswordResetSerializer,
                                                PasswordUpdateSerializer,
                                                TokenSerializer,
                                                UserInfoResponseSerializer)


#TODO BEES-1067: factorize to bb
class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return not request.user or is_anonymous(request.user)

####################################################
# UserDetails
####################################################
class UserDetailsView(mixins.RetrieveModelMixin, GenericAPIView):
    """
    Returns User's details in JSON format.
    Accepts the following GET parameters: token
    Returns the updated UserProfile and/or User object.
    """
    serializer_class = UserInfoResponseSerializer
    permission_classes = (IsAuthenticated,) 

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# class UserPreferenceViewSet(mixins.RetrieveModelMixin,
#                             mixins.UpdateModelMixin,
#                             GenericViewSet):
#     """Return the authenticated User's UserPreferences."""
#     serializer_class = UserPreferenceSerializer

#     def get_object(self):
#         return self.request.user.preference


####################################################
# Log in/out APIs
####################################################
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAnonymous,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    response_serializer = TokenSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login(request)
        return self.get_response()

    def login(self, request):
        self.user = self.serializer.validated_data['user']
        self.token = AuthToken.objects.create(self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(
            self.response_serializer(
                {'token': self.token, 'user': self.user}).data,
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # Delete the specific Token
        if request.auth: # Support Swagger scenarios
            request._auth.delete()

        # Classic Django logout
        logout(request)
        return Response({"success":'Successfully logged out.'},
                        status=status.HTTP_200_OK)


class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # Delete ALL the Tokens for the logged user
        request.user.auth_token_set.all().delete()

        # Classic Django logout
        logout(request)
        return Response({"success": 'Successfully logged out.'},
                        status=status.HTTP_200_OK)


####################################################
# Member serializers
####################################################
#TODO BEES-1068: invalid all tokens after password reset
class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (IsAnonymous,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": SUCCESS_PWD_RESET_EMAIL},
            status=status.HTTP_200_OK
        )



class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (IsAnonymous,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': SUCCESS_PWD_RESET})


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': SUCCESS_PWD_SAVE})


####################################################
# TODO: Social login
####################################################
# from allauth.socialaccount.providers.facebook.views import \
#     FacebookOAuth2Adapter
# from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter


# class TwitterLogin(SocialLoginView):
#     serializer_class = TwitterLoginSerializer
#     adapter_class = TwitterOAuthAdapter
