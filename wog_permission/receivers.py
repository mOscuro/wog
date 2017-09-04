from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from guardian.shortcuts import assign_perm

from wog_permission.constants import AUTHENTICATED_USER_GROUP
from wog_user.models import User
from wog_workout.models import Workout
from wog_permission.constants import (AUTHENTICATED_USER_GROUP,
                                      PERMISSION_WORKOUT_VIEW,
                                      PERMISSION_WORKOUT_MODIFY,
                                      PERMISSION_WORKOUT_ADMIN)


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
        assign_perm(PERMISSION_WORKOUT_ADMIN, instance.creator, instance)
        assign_perm(PERMISSION_WORKOUT_VIEW, instance.creator, instance)
        assign_perm(PERMISSION_WORKOUT_MODIFY, instance.creator, instance)
        Group.objects.create(name='Workout-%s-view' % instance.id)

        if instance.is_public:
            # Give view permission to all authenticated users
            auth_group = Group.objects.get(name=AUTHENTICATED_USER_GROUP)
            assign_perm(PERMISSION_WORKOUT_VIEW, auth_group, instance)