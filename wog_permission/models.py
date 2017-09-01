# -*- coding: utf-8 -*-
"""
Define the Beesbusy custom object-level permissions
and the Beesbusy Permission Groups.
"""
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext as _
from guardian.shortcuts import assign_perm
from rest_framework.exceptions import APIException
from rest_framework.permissions import DjangoObjectPermissions

from wog_permission.constants import (PERMISSION_WORKOUT_ADMIN,
                                      PERMISSION_WORKOUT_MODIFY,
                                      PERMISSION_WORKOUT_VIEW)


####################################################
# WORKOUT PERMISSIONS
####################################################
class WorkoutObjectPermissions(DjangoObjectPermissions):
    """
    Define custom object-level permissions for the workouts.
    Depending on the request HTTP method, the user will need the
    appropriate permission on a given Workout.
    """
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [PERMISSION_WORKOUT_VIEW],
        'HEAD': [PERMISSION_WORKOUT_VIEW],
        'PATCH': [PERMISSION_WORKOUT_ADMIN],
        'POST': [PERMISSION_WORKOUT_ADMIN],
        'PUT': [PERMISSION_WORKOUT_ADMIN],
        'DELETE': [PERMISSION_WORKOUT_ADMIN],
    }

class WorkoutItemsObjectPermissions(DjangoObjectPermissions):
    """
    Define custom object-level permissions for the Workout items
    (rounds, steps, etc.).
    Depending on the request HTTP method, the user will need the
    appropriate permission on a given Workout.
    """
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [PERMISSION_WORKOUT_VIEW],
        'HEAD': [PERMISSION_WORKOUT_VIEW],
        'PATCH': [PERMISSION_WORKOUT_MODIFY],
        'POST': [PERMISSION_WORKOUT_MODIFY],
        'PUT': [PERMISSION_WORKOUT_MODIFY],
        'DELETE': [PERMISSION_WORKOUT_MODIFY],
    }
