
from rest_framework.permissions import DjangoObjectPermissions

PERMISSION_WORKOUT_VIEW = 'workout.view_workout'
PERMISSION_WORKOUT_ADD = 'workout.add_workout'
PERMISSION_WORKOUT_MODIFY = 'workout.change_workout'
PERMISSION_WORKOUT_DELETE = 'workout.delete_workout'

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


PERMISSION_ROUNDS_ADD = 'workout.add_workout_rounds'
PERMISSION_ROUNDS_MODIFY = 'workout.change_workout_rounds'
PERMISSION_ROUNDS_DELETE = 'workout.delete_workout_rounds'

class RoundObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [PERMISSION_ROUNDS_ADD],
        'PUT': [PERMISSION_ROUNDS_MODIFY],
        'PATCH': [PERMISSION_ROUNDS_MODIFY],
        'DELETE': [PERMISSION_ROUNDS_DELETE],
    }


PERMISSION_STEPS_ADD = 'workout.add_workout_steps'
PERMISSION_STEPS_MODIFY = 'workout.change_workout_steps'
PERMISSION_STEPS_DELETE = 'workout.delete_workout_steps'

class StepObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [PERMISSION_WORKOUT_VIEW],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [PERMISSION_STEPS_ADD],
        'PUT': [PERMISSION_STEPS_MODIFY],
        'PATCH': [PERMISSION_STEPS_MODIFY],
        'DELETE': [PERMISSION_STEPS_DELETE],
    }
