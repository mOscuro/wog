from __future__ import absolute_import

from allauth.account.adapter import get_adapter
from allauth.account.forms import BaseSignupForm, PasswordField, SetPasswordField
from allauth.account.utils import setup_user_email
from django import forms
from django.utils.translation import ugettext_lazy as _

from wogether import settings


class SignupForm(BaseSignupForm):
    first_name = forms.CharField(max_length=30,
                                 label=_("First name"),
                                 widget=forms.TextInput(
                                     attrs={'placeholder': _('First name')}))
    last_name = forms.CharField(max_length=30,
                                label=_("Last name"),
                                widget=forms.TextInput(
                                    attrs={'placeholder': _('Last name')}))
    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)"))
    confirmation_key = forms.CharField(max_length=40,
                                       required=False,
                                       widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        if not getattr(settings, 'SIGNUP_PASSWORD_VERIFICATION', True):
            del self.fields["password2"]

    def clean(self):
        super(SignupForm, self).clean()
        if getattr(settings, 'SIGNUP_PASSWORD_VERIFICATION', True) \
                and "password1" in self.cleaned_data \
                and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] \
                    != self.cleaned_data["password2"]:
                raise forms.ValidationError(_('You must type the same password'
                                              ' each time.'))
        return self.cleaned_data

    # def clean_first_name(self):
    #     if ""

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user
