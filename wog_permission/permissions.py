# -*- coding: utf-8 -*-
# TODO: ADAPT FROM BB TO WOG
"""Django permission classes. Can be added to an APIView permission_classes tuple."""
from django.conf import settings
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from wog_permission.models import WorkoutItemsObjectPermissions
from wog_workout.models import Workout

class IsAuthorizedForModel(IsAuthenticated):
    """
    Custom BasePermission that verifies the User has the proper permissions:
    -   Must be authenticated
    -   Must have object-permissions on the Model instance corresponding to the HTTP method
    It is similar to having a DjangoObjectPermissionsFilter for a related model.

    This is an ABSTRACT class that should not be used as is.
    Inheriting classes should define the following class attributes:
    -   pk_kwarg = The name of the kwarg in the Django URL format
    -   klass = The class Model to use as permission verification
    -   klass_permission = The DjangoObjectPermissions for the specified Model
    """
    def has_permission(self, request, view):
        """Look for the referenced object and verify the permissions."""
        # Verify the user is Authenticated
        if not super().has_permission(request, view):
            raise Http404

        # Check if the referenced account exists
        pk_kwarg = view.kwargs.get(self.pk_kwarg)
        if pk_kwarg is None:
            # If there is no correct PK refuse unless it's Swagger
            if settings.DEBUG and request.path == '/docs/':
                return True
            raise Http404
        instance = get_object_or_404(self.klass.objects.all(), pk=pk_kwarg)

        # Verify the user has access to the account for this request method
        return self.klass_permission.has_object_permission(request, view, instance)


class IsAuthorizedForWorkout(IsAuthorizedForModel):
    """Verify the user has the authorizations on the Project specified in the URL."""
    pk_kwarg = 'workout_pk'
    klass = Workout
    klass_permission = WorkoutItemsObjectPermissions()


# class IsAuthorizedForProjectMember(IsAuthorizedForModel):
#     """Verify the user has Admin permission on the Project specified in the URL."""
#     pk_kwarg = 'project_pk'
#     klass = Project
#     klass_permission = ProjectObjectPermissions()
