from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from guardian.shortcuts import assign_perm

from permission.constants import AUTHENTICATED_USER_GROUP
from user_account.models import User
from workout.models import Workout
from workout.constants import PUBLIC


######################################
# AT USER CREATION
######################################
@receiver(post_save, sender=User)
def give_user_standard_model_permissions(sender, instance, **kwargs):
    if kwargs.get('created', True):
        auth_group = Group.objects.get(name=AUTHENTICATED_USER_GROUP)
        auth_group.user_set.add(instance)

######################################
# AT WORKOUT CREATION
######################################
@receiver(post_save, sender=Workout)
def create_workout_permissions(sender, instance, **kwargs):
    """
    Create specific permission for the creator of a workout.
    If it is a shared workout, all authenticated users can view the workout
    """
    if kwargs.get('created', True):
        creator = instance.creator
        assign_perm('workout.view_workout', creator, instance)
        assign_perm('workout.change_workout', creator, instance)
        assign_perm('workout.delete_workout', creator, instance)
        
        assign_perm('workout.add_workout_round', creator, instance)
        assign_perm('workout.change_workout_round', creator, instance)
        assign_perm('workout.delete_workout_round', creator, instance)

        assign_perm('workout.add_workout_step', creator, instance)
        assign_perm('workout.change_workout_step', creator, instance)
        assign_perm('workout.delete_workout_step', creator, instance)

        if instance.type==PUBLIC:
            auth_group = Group.objects.get(name=AUTHENTICATED_USER_GROUP)
            assign_perm('workout.view_workout', auth_group, instance)