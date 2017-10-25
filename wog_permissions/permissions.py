
from django.apps import apps
from django.conf import settings
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated

from wog_permissions.constants import (PERMISSION_SESSION_VIEW, PERMISSION_PROGRESS_VIEW, PERMISSION_PROGRESS_MODIFY,
                                        SESSION_INVITED_GROUP_ID)
from wog_permissions.helpers import get_permission_profile
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
        """
        - Only session creator can update, delete, or invite other users.
        - Invited users can join to compete, or just watch progressions.
        - Other users can join as well but only if session is public.
        - Specific view exists to let user quit groups.
        """
        
        # Only spectator, competitor or invited user can quit session. Session creator cannot quit.
        if view.action in ['quit']:
            return request.user.session_permissions.filter(session=obj).exists() and request.user != obj.creator

        # To be authorize to execute session of workout, user needs to be in invited group. Or session is public.
        if view.action in ['compete', 'watch']:
            get_permission_profile(obj, SESSION_INVITED_GROUP_ID)
            return request.user.session_permissions.filter(session=obj).exists() or obj.is_public

        # Only session creator can modify or delete it
        if view.action in ['update', 'partial_update', 'destroy', 'invite']:
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