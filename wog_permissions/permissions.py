
from django.apps import apps
from django.conf import settings
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated

from wog_permissions.constants import PERMISSION_SESSION_VIEW, PERMISSION_PROGRESS_VIEW, PERMISSION_PROGRESS_MODIFY
from wog_workout.models import Workout, WorkoutSession, WorkoutProgression


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


class IsAuthorizedForWorkoutSession(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Only session creator can modify or delete it
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj.creator
        
        if view.action in ['retrieve', 'OPTIONS', 'HEAD']:
            return request.user.has_perm(PERMISSION_SESSION_VIEW, obj)

        return view.action in ['list', 'create']


class IsAuthorizedForWorkoutProgression(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Only session creator can modify or delete it
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.has_perm(PERMISSION_PROGRESS_MODIFY, obj.session)
        
        elif view.action in ['list', 'retrieve', 'OPTIONS', 'HEAD']:
            return request.user.has_perm(PERMISSION_PROGRESS_VIEW, obj.session)
        
        else:
            return False