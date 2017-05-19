from django.conf.urls import url
from django.views.generic.base import TemplateView

from user_account.registration.views import SendVerificationEmailView, RegisterView, \
    VerifyEmailView


urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='rest_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    url(r'^send-verification-email/$', SendVerificationEmailView.as_view(), name='rest_send_verification_email'),

    # Bypass view from Django Allauth
    url(r"^confirm-email/$", TemplateView.as_view(), name="account_email_verification_sent"),
]
