from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^verify-email/(?P<key>\w+)$',
        TemplateView.as_view(),
        name='account_confirm_email'),

    url(r"^reset-password/(?P<uidb36>[0-9A-Za-z]+)/(?P<key>.+)$",
        TemplateView.as_view(),
        name="account_reset_password_from_key"),

    # Front-end Registration URL
    url(r"^register/$",
        TemplateView.as_view(),
        name="front_register"),
]
