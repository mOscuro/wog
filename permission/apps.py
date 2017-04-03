from django.apps import AppConfig


class PermissionConfig(AppConfig):
    name = 'permission'

    def ready(self):
        import permission.receivers  # @UnusedImport