import hashlib
import time

from allauth.account import app_settings as allauth_settings
from allauth.account.forms import SetPasswordForm, UserTokenForm
from allauth.account.utils import send_email_confirmation
from allauth.utils import get_current_site
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from user_account.authentication.forms import ResetPasswordForm
from user_account.models import User


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _get_login_attempts_cache_key(self, **credentials):
        site = get_current_site(self.context['request'])
        login = credentials.get('email', credentials.get('username', ''))
        login_key = hashlib.sha256(login.encode('utf8')).hexdigest()
        return 'allauth/login_attempts@{site_id}:{login}'.format(
            site_id=site.pk,
            login=login_key)

    def pre_authenticate(self, **credentials):
        if allauth_settings.LOGIN_ATTEMPTS_LIMIT:
            cache_key = self._get_login_attempts_cache_key(**credentials)
            login_data = cache.get(cache_key, None)
            if login_data:
                dt = timezone.now()
                current_attempt_time = time.mktime(dt.timetuple())
                if len(login_data) >= allauth_settings.LOGIN_ATTEMPTS_LIMIT and current_attempt_time < \
                        (login_data[-1] + allauth_settings.LOGIN_ATTEMPTS_TIMEOUT):
                    raise exceptions.AuthenticationFailed(
                        _('Too many failed login attempts. Try again later.'))

    def authenticate(self, **credentials):
        """Only authenticates, does not actually login. See `login`"""
        self.pre_authenticate(**credentials)
        user = authenticate(**credentials)
        if user:
            cache_key = self._get_login_attempts_cache_key(**credentials)
            cache.delete(cache_key)
        else:
            self.authentication_failed(**credentials)
        return user

    def authentication_failed(self, **credentials):
        cache_key = self._get_login_attempts_cache_key(**credentials)
        data = cache.get(cache_key, [])
        dt = timezone.now()
        data.append(time.mktime(dt.timetuple()))
        cache.set(cache_key, data, allauth_settings.LOGIN_ATTEMPTS_TIMEOUT)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authentication through email
        user = self.authenticate(email=email, password=password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            email_address = user.emailaddress_set.get(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context['request']._request, user)
                raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class CustomPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = ResetPasswordForm

    def get_email_options(self):
        """ Override this method to change default e-mail options
        """
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        return self.reset_form.clean_email()

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm
    token_generator = default_token_generator

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}
        token_form = UserTokenForm(data={'uidb36': attrs['uid'], 'key': attrs['token']})

        if not token_form.is_valid():
            self.reset_user = None
            raise serializers.ValidationError({'non_field_errors': ['The password reset token was invalid.']})
        else:
            self.reset_user = token_form.reset_user

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.reset_user, data=attrs
        )
        if not self.set_password_form.is_valid():
            # Coverage comment :
            # Must keep this verification in case we use a custom ResetPasswordForm
            # that would not perform the verification
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        self.set_password_form.save()


class CustomPasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=128)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(CustomPasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not getattr(settings, 'LOGOUT_ON_PASSWORD_CHANGE', False):
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
        else:
            try:
                self.request.user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):  # If we don't use token type authentication
                pass


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = ('email',)
