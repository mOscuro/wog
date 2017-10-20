from django.contrib.auth.models import Group
from django.db import models
from guardian.shortcuts import assign_perm
from rest_framework.exceptions import APIException

from wogether.settings import AUTH_USER_MODEL
from wog_permissions.constants import (SESSION_DEFAULT_PERMISSION_ID,
                                       SESSION_INVITED_PERMISSION_ID,
                                       SESSION_SPECTATOR_PERMISSION_ID,
                                       SESSION_COMPETITOR_PERMISSION_ID,
                                       PERMISSION_SESSION_INVITED,
                                       PERMISSION_SESSION_SPECTATOR,
                                       PERMISSION_SESSION_COMPETITOR)


PERMISSION_NAME_INVITED = 'invited'
PERMISSION_NAME_SPECTATOR = 'spectator'
PERMISSION_NAME_COMPETITOR = 'competitor'

SESSION_PERMISSION_PROFILE_CHOICES = (
    (SESSION_INVITED_PERMISSION_ID, PERMISSION_NAME_INVITED),
    (SESSION_SPECTATOR_PERMISSION_ID, PERMISSION_NAME_SPECTATOR),
    (SESSION_COMPETITOR_PERMISSION_ID, PERMISSION_NAME_COMPETITOR),
)

class WorkoutSessionPermissionGroup(Group):
    """
    3 groups are created for each WorkoutSession:
    - Invited : users in this type of group are invited, no permission on progression
    - Spectator : users get read only permissions on the progessions of the session
    - Competitor : users get the permissions to get, create and delete their progression
    """
    session = models.ForeignKey('wog_workout.WorkoutSession', related_name='permission_groups')
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name='session_permissions')
    profile_type = models.IntegerField(
        choices=SESSION_PERMISSION_PROFILE_CHOICES,
        default=SESSION_DEFAULT_PERMISSION_ID)

    class Meta:
        unique_together = ('session', 'profile_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the name of the group based on the profile type
        self.profile_type_name = WorkoutSessionPermissionGroup._get_profile_type_name(self.profile_type)
        # Uses `_id` to avoid making a call to the DB
        self.name = 'workout#%d-session#%d-%s' % (self.session.workout_id, self.session_id, self.profile_type_name)


    def assign_perms(self):
        """Assign the appropriate ProjectPermissions to this group."""
        for permission in WorkoutSessionPermissionGroup._get_permission_codenames(self.profile_type):
            assign_perm(permission, self, self.session)

    @staticmethod
    def _get_profile_type_name(profile_type: int) -> str:
        """Return the localized name of the profile type."""
        if profile_type == SESSION_INVITED_PERMISSION_ID:
            return PERMISSION_NAME_INVITED
        if profile_type == SESSION_SPECTATOR_PERMISSION_ID:
            return PERMISSION_NAME_SPECTATOR
        if profile_type == SESSION_COMPETITOR_PERMISSION_ID:
            return PERMISSION_NAME_COMPETITOR
        raise APIException('Wrong permission type for session group')

    @staticmethod
    def _get_permission_codenames(profile_type) -> list:
        """Return the list of permissions assigned to the given profile type."""
        perms = []
        if profile_type == SESSION_INVITED_PERMISSION_ID:
            perms.append(PERMISSION_SESSION_INVITED)
        if profile_type == SESSION_SPECTATOR_PERMISSION_ID:
            perms.append(PERMISSION_SESSION_SPECTATOR)
        if profile_type == SESSION_COMPETITOR_PERMISSION_ID:
            perms.append(PERMISSION_SESSION_COMPETITOR)
        return perms