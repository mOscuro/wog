from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm

from wog_permissions.constants import (SESSION_INVITED_GROUP_ID,
                                       SESSION_SPECTATOR_GROUP_ID,
                                       SESSION_COMPETITOR_GROUP_ID,
                                       PERMISSION_SESSION_MODIFY)
from wog_permissions.helpers import get_permission_profile
from wog_workout.models import WorkoutSession


@receiver(post_save, sender=WorkoutSession)
def give_user_session_permissions(sender, instance, **kwargs):
    """
    Create the WorkoutSessionPermission groups for the newly created WorkoutSession
    and add the creator to the competitor group.
    """
    if kwargs.get('created', True):
        # Create the ProjectPermissionGroup for every type of group
        get_permission_profile(instance, SESSION_INVITED_GROUP_ID)
        get_permission_profile(instance, SESSION_SPECTATOR_GROUP_ID)
        competitor_group = get_permission_profile(instance, SESSION_COMPETITOR_GROUP_ID)

        # Give session creator modify permissions
        assign_perm(PERMISSION_SESSION_MODIFY, instance.creator, instance)

        # Add session creator to competitor group
        instance.creator.groups.add(competitor_group)
        competitor_group.users.add(instance.creator)