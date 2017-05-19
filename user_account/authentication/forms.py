from allauth.account.adapter import get_adapter
from allauth.account.utils import filter_users_by_email, user_pk_to_url_str
from allauth.utils import get_current_site
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _

from wogether.core.urlresolvers import reverse


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(
        label=_('E-mail'),
        required=True,
        widget=forms.TextInput(attrs={
            "type": "email",
            "size": "30",
            "placeholder": _('E-mail address'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        email = get_adapter().clean_email(email)
        return email

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]

        self.users = filter_users_by_email(email)
        if not self.users:
            # The system is unable to find a user with the given email
            # So we send a mail to this address to propose to register
            
            url = reverse("front_register")
            
            context = {"current_site": current_site,
                       "register_url": url,
                       "request": request}

            get_adapter(request).send_mail(
                'account/email/unknown_user_password_reset',
                email,
                context)
            
            return email

        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            url = reverse("account_reset_password_from_key",
                          kwargs=dict(uidb36=user_pk_to_url_str(user),
                                      key=temp_key))

            context = {"current_site": current_site,
                       "user": user,
                       "password_reset_url": url,
                       "request": request}

            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context)
        return self.cleaned_data["email"]
