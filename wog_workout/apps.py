from django.apps import AppConfig


class WorkoutConfig(AppConfig):
    name = 'wog_workout'

    def ready(self):
        import wog_workout.receivers  # @UnusedImport