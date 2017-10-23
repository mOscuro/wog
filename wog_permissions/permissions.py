
from django.apps import apps
from django.conf import settings
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated

from wog_permissions.models import WorkoutProgressionObjectPermissions
from wog_workout.models import Workout, WorkoutSession, WorkoutProgression


class IsAuthorizedForProgession(IsAuthenticated):
    """  """
    def has_permission(self, request, view):
        """Look for the referenced object and verify the permissions."""
        # Verify the user is Authenticated
        if not super().has_permission(request, view):
            raise Http404

        # Check if the referenced account exists
        pk_kwarg = view.kwargs.get('session_pk')
        if pk_kwarg is None:
            # If there is no correct PK refuse unless it's Swagger
            if settings.DEBUG and request.path == '/docs/':
                return True
            raise Http404
        instance = get_object_or_404(WorkoutSession.objects.all(), pk=pk_kwarg)
        # Verify the user has access to the account for this request method
        return WorkoutProgressionObjectPermissions().has_object_permission(request, view, instance)


#===============================================================================
# CUSTOM HOMEMADE PERMISSIONS
#===============================================================================

class IsWorkoutCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):

        # For Workout Viewset
        if isinstance(obj, apps.get_model('wog_workout', 'Workout')):
            workout_instance = obj

        # For Round Viewset
        if isinstance(obj, apps.get_model('wog_round', 'Round')):
            workout_instance = obj.workout

        # For Step Viewset
        if isinstance(obj, apps.get_model('wog_round', 'Step')):
            workout_instance = obj.round.workout

        return workout_instance.creator == request.user\
                or (request.method in permissions.SAFE_METHODS and workout_instance.is_public)


class IsSessionCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.creator == request.user\
                or (request.method in permissions.SAFE_METHODS and obj.is_public)
