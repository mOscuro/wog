from django.apps import AppConfig


class UserAccountConfig(AppConfig):
    name = 'wog_user'

    def ready(self):
        import wog_user.receivers  # @UnusedImport