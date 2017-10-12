
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.account.views import ConfirmEmailView
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_user_model
from knox.models import AuthToken
from rest_framework import status
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from wog_user.registration.serializers import RegisterSerializer,\
    SendVerificationEmailSerializer, VerifyEmailSerializer
from wog_user.authentication.views import IsAnonymous
from wog_user.authentication.serializers import TokenSerializer


class RegisterView(CreateAPIView):
    """
    API view used to register a new user.
    """
    permission_classes = (IsAnonymous,)
    serializer_class = RegisterSerializer
    token_model = AuthToken

    def create(self, request, *args, **kwargs):
        # Verify creation is possible
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the user and a first AuthToken
        user = serializer.save(self.request)
        token = AuthToken.objects.create(user)
        data = {}
        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        if allauth_settings.EMAIL_VERIFICATION != \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            data = TokenSerializer({'token': token, 'user': user}).data
        return Response(data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView, ConfirmEmailView):
    """
    API view used to confirm the email address of a newly registered user.
    """
    serializer_class = VerifyEmailSerializer
    permission_classes = (IsAnonymous,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        # Accept all pending MembershipRequests
        user = confirmation.email_address.user
        return Response({'message': [_('ok')]}, status=status.HTTP_200_OK)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            queryset = self.get_expired_queryset()
            try:
                confirmation = queryset.get(key=self.kwargs["key"].lower())
                send_email_confirmation(self.request._request, confirmation.email_address.user)
                raise ValidationError(
                    {'non_field_errors': [_('The link has expired, a new verification email has just been sent.')]})
            except EmailConfirmation.DoesNotExist:
                raise ValidationError({'non_field_errors': [_('The link is invalid.')]})

    def get_expired_queryset(self):
        qs = EmailConfirmation.objects.all_expired()
        qs = qs.select_related("email_address__user")
        return qs


class SendVerificationEmailView(CreateAPIView):
    """
    API view used to send again a verification email to a user who registered and does not have verified
    his email address.

    Additional notes:
    * if a user has already verified his email address, no email is sent (HTTP code 200)
    * if the email address does not correspond to a user, no error message is sent ((HTTP code 200)
    """
    serializer_class = SendVerificationEmailSerializer
    permission_classes = (IsAnonymous,)

    def post(self, request, *args, **kwargs):
        serializer = SendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_user_model().objects.get(email=serializer.validated_data['email'])
            email_address = EmailAddress.objects.get_for_user(user, serializer.validated_data['email'])
            if not email_address.verified:
                email_address.send_confirmation(request)
            else:
                # User has already a verified email, verification email should not be sent
                pass
        except get_user_model().DoesNotExist:
            # there is no user corresponding to this email address, do not send anything
            pass

        return Response({'message': _('ok')}, status=status.HTTP_200_OK)


# class SocialLoginView(rest_auth_views.SocialLoginView):
#     """
#     class used for social authentications
#     example usage for facebook with access_token
#     ::

#         from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

#         class FacebookLogin(SocialLoginView):
#             adapter_class = FacebookOAuth2Adapter


#     example usage for facebook with code:
#     ::

#         from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
#         from allauth.socialaccount.providers.oauth2.client import OAuth2Client

#         class FacebookLogin(SocialLoginView):
#             adapter_class = FacebookOAuth2Adapter
#              client_class = OAuth2Client
#              callback_url = 'localhost:8000'

#     """
#     permission_classes = (IsAnonymous,)
#     serializer_class = SocialLoginSerializer
