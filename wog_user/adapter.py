from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.utils.translation import ugettext_lazy as _

from wog_wogether.core.urlresolvers import reverse
#from bb_user_preference.models import Preference


class MyAccountAdapter(DefaultAccountAdapter):

    def clean_password(self, password):
        """
        Validates a password. You can hook into this if you want to
        restric the allowed password choices.
        """
        min_length = allauth_settings.PASSWORD_MIN_LENGTH
        if len(password) < min_length:
            raise forms.ValidationError(_('Password must be a minimum of {0} '
                                          'characters.').format(min_length))
        return password

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "account_confirm_email",
            args=[emailconfirmation.key])
        return url
    
    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(request, user, form, commit)
        #Preference.objects.create(user=user, ui_language=request.LANGUAGE_CODE)
        return user

