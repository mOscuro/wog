from django.apps import AppConfig


class WorkoutConfig(AppConfig):
    name = 'workout'

    def ready(self):
        import workout.receivers  # @UnusedImport