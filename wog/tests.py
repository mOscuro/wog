import logging
import random

from allauth.account.models import EmailAddress
from django.conf import settings
from django.test import TestCase
from django.test.runner import DiscoverRunner
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.test import APIClient, APITestCase

from wog.management.commands.create_permissions import create_permissions
from wog.management.commands.create_data import init_catalog
from wog_workout.models import Workout, WorkoutSession
from wog_user.models import User


class WogetherTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        logging.disable(logging.ERROR)
        return super().run_tests(test_labels, extra_tests, **kwargs)


class WogetherTestMixin:

    @classmethod
    def create_user(cls, i=1):
        user = User.objects.create_user(email='user%d@beesbusy.com' % i,
                                        username='user%d' % i,
                                        first_name='John %d' % i,
                                        last_name='Doe %d' % i,
                                        password="strong_password")
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        # Preference.objects.create(user=user, ui_language=random.choice(settings.LANGUAGES)[0])
        return user

    @classmethod
    def create_custom_user(cls, **kwargs):
        user = User.objects.create_user(email=kwargs.get('email', None),
                                        first_name=kwargs.get('first_name', None),
                                        last_name=kwargs.get('last_name', None),
                                        password=kwargs.get('password', None))
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        # Preference.objects.create(user=user, ui_language=random.choice(settings.LANGUAGES)[0])
        return user

    @classmethod
    def create_superuser(cls, **kwargs):
        user = User.objects.create_superuser(email=kwargs.get('email', None),
                                             first_name=kwargs.get('first_name', None),
                                             last_name=kwargs.get('last_name', None),
                                             password=kwargs.get('password', None))
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        # Preference.objects.create(user=user, ui_language=random.choice(settings.LANGUAGES)[0])
        return user

    @classmethod
    def create_workout(cls, **kwargs):
        return Workout.objects.create(name=kwargs.get('name', None),
                                      creator=kwargs.get('creator', None),
                                      is_active=kwargs.get('is_active', True),
                                      is_staff=kwargs.get('is_staff', False),
                                      is_public=kwargs.get('is_public', False))

    @classmethod
    def create_session(cls, **kwargs):
        return WorkoutSession.objects.create(workout=kwargs.get('workout', None),
                                             creator=kwargs.get('creator', None),
                                             start=kwargs.get('start', None),
                                             is_public=kwargs.get('is_public', False))

class WogetherTestCase(TestCase, WogetherTestMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        create_permissions()
        init_catalog()

class WogetherAPITestCase(APITestCase, WogetherTestMixin):
    client_class = APIClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        create_permissions()
        init_catalog()

