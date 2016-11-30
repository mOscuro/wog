from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from . import signals