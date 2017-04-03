from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from workout.models import Workout


class GenericProjectPermissionViewSet(viewsets.GenericViewSet):
    object_permission_class = None
    response_serializer_class = None

    def get_workout(self, workout_pk=None):
        """
         Look for the referenced workout
         """
        # Check if the referenced workout exists
        workout = get_object_or_404(Workout.objects.all(), pk=workout_pk)
        self.check_specific_permissions(workout)
        return workout

    def get_object_permission(self):
        object_permission_class = self.get_object_permission_class()
        return object_permission_class()

    def get_object_permission_class(self):
        assert self.object_permission_class is not None, (
            "'%s' should either include a `object_permission_class` attribute, "
            "or override the `get_object_permission_class()` method."
            % self.__class__.__name__
        )
        return self.object_permission_class

    def check_specific_permissions(self, workout):
        permission = self.get_object_permission()
        if not permission.has_object_permission(self.request, self, workout):
            self.permission_denied(
                self.request, message=getattr(permission, 'message', None)
            )

    def get_response_serializer(self, *args, **kwargs):
        response_serializer_class = self.get_response_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return response_serializer_class(*args, **kwargs)

    def get_response_serializer_class(self):
        if self.response_serializer_class is not None:
            return self.response_serializer_class
        else:
            return self.serializer_class
