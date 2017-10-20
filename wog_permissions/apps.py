from django.apps import AppConfig


class SessionPermissionsConfig(AppConfig):
    name = 'wog_permissions'

    def ready(self):
        import wog_permissions.receivers  # @UnusedImport