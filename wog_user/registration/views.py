from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import send_email_confirmation
from allauth.utils import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration import views as rest_auth_views
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from wog_user.registration.serializers import SendVerificationEmailSerializer
from wog_user.authentication.views import IsAnonymous

class RegisterView(rest_auth_views.RegisterView):
    """
    API view used to register a new user.
    """
    permission_classes = (IsAnonymous,)


class VerifyEmailView(rest_auth_views.VerifyEmailView):
    """
    API view used to confirm the email address of a newly registered user.
    """
    serializer_class = VerifyEmailSerializer
    permission_classes = (IsAnonymous,)

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


class SocialLoginView(rest_auth_views.SocialLoginView):
    """
    class used for social authentications
    example usage for facebook with access_token
    ::

        from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

        class FacebookLogin(SocialLoginView):
            adapter_class = FacebookOAuth2Adapter


    example usage for facebook with code:
    ::

        from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
        from allauth.socialaccount.providers.oauth2.client import OAuth2Client

        class FacebookLogin(SocialLoginView):
            adapter_class = FacebookOAuth2Adapter
             client_class = OAuth2Client
             callback_url = 'localhost:8000'

    """
