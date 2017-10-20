from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from wog_permissions.constants import (SESSION_INVITED_PERMISSION_ID,
                                       SESSION_SPECTATOR_PERMISSION_ID,
                                       SESSION_COMPETITOR_PERMISSION_ID)
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
        print('WorkoutSession created')
        get_permission_profile(instance, SESSION_INVITED_PERMISSION_ID)
        get_permission_profile(instance, SESSION_SPECTATOR_PERMISSION_ID)
        competitor_group = get_permission_profile(instance, SESSION_COMPETITOR_PERMISSION_ID)

        instance.creator.groups.add(competitor_group)
        competitor_group.users.add(instance.creator)