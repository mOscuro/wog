
from rest_framework.permissions import DjangoObjectPermissions

PERMISSION_WORKOUT_VIEW = 'wog_workout.view_workout'
PERMISSION_WORKOUT_ADD = 'wog_workout.add_workout'
PERMISSION_WORKOUT_MODIFY = 'wog_workout.change_workout'
PERMISSION_WORKOUT_DELETE = 'wog_workout.delete_workout'

class WorkoutObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [PERMISSION_WORKOUT_ADD],
        'PUT': [PERMISSION_WORKOUT_MODIFY],
        'PATCH': [PERMISSION_WORKOUT_MODIFY],
        'DELETE': [PERMISSION_WORKOUT_DELETE],
    }


PERMISSION_ROUND_ADD = 'workout.add_workout_round'
PERMISSION_ROUND_MODIFY = 'workout.change_workout_round'
PERMISSION_ROUND_DELETE = 'workout.delete_workout_round'

class RoundObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [PERMISSION_ROUND_ADD],
        'PUT': [PERMISSION_ROUND_MODIFY],
        'PATCH': [PERMISSION_ROUND_MODIFY],
        'DELETE': [PERMISSION_ROUND_DELETE],
    }


PERMISSION_STEP_ADD = 'workout.add_workout_step'
PERMISSION_STEP_MODIFY = 'workout.change_workout_step'
PERMISSION_STEP_DELETE = 'workout.delete_workout_step'

class StepObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [PERMISSION_STEP_ADD],
        'PUT': [PERMISSION_STEP_MODIFY],
        'PATCH': [PERMISSION_STEP_MODIFY],
        'DELETE': [PERMISSION_STEP_DELETE],
    }
