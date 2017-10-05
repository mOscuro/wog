from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from guardian.shortcuts import assign_perm

from wog_user.models import User
from wog_workout.models import Workout
from wog_workout.constants import (WOG_USER_GROUP_NAME,
                                      PERMISSION_WORKOUT_VIEW,
                                      PERMISSION_WORKOUT_MODIFY)


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
        # Creator of the workout is able to view and modify his workout
        assign_perm(PERMISSION_WORKOUT_VIEW, instance.creator, instance)
        assign_perm(PERMISSION_WORKOUT_MODIFY, instance.creator, instance)
        # TODO: See if usefull
        # Group.objects.create(name='Workout-%s-view' % instance.id)

        if instance.is_public:
            # Give view permission to all authenticated users
            auth_group = Group.objects.get(name=WOG_USER_GROUP_NAME)
            assign_perm(PERMISSION_WORKOUT_VIEW, auth_group, instance)