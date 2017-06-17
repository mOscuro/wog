from django.apps import AppConfig


class PermissionConfig(AppConfig):
    name = 'wog_permission'

    def ready(self):
        import wog_permission.receivers  # @UnusedImport