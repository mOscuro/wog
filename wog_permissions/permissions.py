
from rest_framework import permissions
from rest_framework.permissions import DjangoObjectPermissions
from django.apps import apps

from wog_workout.constants import (PERMISSION_WORKOUT_VIEW, PERMISSION_WORKOUT_ADD,
                                  PERMISSION_WORKOUT_MODIFY, PERMISSION_WORKOUT_DELETE)


class WorkoutObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': ['wog_workout.%s' % PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['wog_workout.%s' % PERMISSION_WORKOUT_ADD],
        'PUT': ['wog_workout.%s' % PERMISSION_WORKOUT_MODIFY],
        'PATCH': ['wog_workout.%s' % PERMISSION_WORKOUT_MODIFY],
        'DELETE': ['wog_workout.%s' % PERMISSION_WORKOUT_DELETE],
    }


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

#===============================================================================
# PERMISSIONS MAPPING FOR WORKOUT REQUESTS
#===============================================================================

# PERMISSION_ROUND_ADD = 'workout.add_workout_round'
# PERMISSION_ROUND_MODIFY = 'workout.change_workout_round'
# PERMISSION_ROUND_DELETE = 'workout.delete_workout_round'

# class RoundObjectPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': [PERMISSION_WORKOUT_VIEW],
#         'OPTIONS': [],
#         'HEAD': [],
#         'POST': [PERMISSION_ROUND_ADD],
#         'PUT': [PERMISSION_ROUND_MODIFY],
#         'PATCH': [PERMISSION_ROUND_MODIFY],
#         'DELETE': [PERMISSION_ROUND_DELETE],
#     }


# PERMISSION_STEP_ADD = 'workout.add_workout_step'
# PERMISSION_STEP_MODIFY = 'workout.change_workout_step'
# PERMISSION_STEP_DELETE = 'workout.delete_workout_step'

# class StepObjectPermissions(DjangoObjectPermissions):
#     perms_map = {
#         'GET': [PERMISSION_WORKOUT_VIEW],
#         'OPTIONS': [],
#         'HEAD': [],
#         'POST': [PERMISSION_STEP_ADD],
#         'PUT': [PERMISSION_STEP_MODIFY],
#         'PATCH': [PERMISSION_STEP_MODIFY],
#         'DELETE': [PERMISSION_STEP_DELETE],
#     }
