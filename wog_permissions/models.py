from django.contrib.auth.models import Group
from django.db import models
from guardian.shortcuts import assign_perm
from rest_framework.exceptions import APIException
from rest_framework.permissions import DjangoObjectPermissions

from wogether.settings import AUTH_USER_MODEL
from wog_workout.constants import (PERMISSION_WORKOUT_VIEW, PERMISSION_WORKOUT_ADD,
                                  PERMISSION_WORKOUT_MODIFY, PERMISSION_WORKOUT_DELETE)
from wog_permissions.constants import (SESSION_DEFAULT_GROUP_ID,
                                       SESSION_INVITED_GROUP_ID,
                                       SESSION_SPECTATOR_GROUP_ID,
                                       SESSION_COMPETITOR_GROUP_ID,
                                       PERMISSION_SESSION_VIEW, PERMISSION_SESSION_MODIFY,
                                       PERMISSION_PROGRESS_VIEW, PERMISSION_PROGRESS_MODIFY)


class WorkoutProgressionObjectPermissions(DjangoObjectPermissions):
    """
    Define custom object-level permissions for the project items
    (tasks, tasklist, etc.). Those permissions are different than the
    ProjectObjectPermissions.
    Depending on the request HTTP method, the user will need the
    appropriate permission on a given project.
    """
    perms_map = {
        'GET': [PERMISSION_PROGRESS_VIEW],
        'OPTIONS': [PERMISSION_PROGRESS_VIEW],
        'HEAD': [PERMISSION_PROGRESS_VIEW],
        'PATCH': [PERMISSION_PROGRESS_MODIFY],
        'POST': [PERMISSION_PROGRESS_MODIFY],
        'PUT': [PERMISSION_PROGRESS_MODIFY],
        'DELETE': [PERMISSION_PROGRESS_MODIFY],
    }

####################################################
# PERMISSION GROUPS (profiles)
####################################################
INVITED_GROUP_NAME = 'guests'
SPECTATOR_GROUP_NAME = 'spectators'
COMPETITOR_GROUP_NAME = 'competitors'

SESSION_PERMISSION_PROFILE_CHOICES = (
    (SESSION_INVITED_GROUP_ID, INVITED_GROUP_NAME),
    (SESSION_SPECTATOR_GROUP_ID, SPECTATOR_GROUP_NAME),
    (SESSION_COMPETITOR_GROUP_ID, COMPETITOR_GROUP_NAME),
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
        default=SESSION_DEFAULT_GROUP_ID)

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
        if profile_type == SESSION_INVITED_GROUP_ID:
            return INVITED_GROUP_NAME
        if profile_type == SESSION_SPECTATOR_GROUP_ID:
            return SPECTATOR_GROUP_NAME
        if profile_type == SESSION_COMPETITOR_GROUP_ID:
            return COMPETITOR_GROUP_NAME
        raise APIException('Wrong permission type for session group')

    @staticmethod
    def _get_permission_codenames(profile_type) -> list:
        """Return the list of permissions assigned to the given profile type."""
        perms = []
        # Only guest
        if profile_type == SESSION_INVITED_GROUP_ID:
            perms.append(PERMISSION_SESSION_VIEW)
        # Spectator mode
        if profile_type == SESSION_SPECTATOR_GROUP_ID:
            perms.append(PERMISSION_SESSION_VIEW)
            perms.append(PERMISSION_PROGRESS_VIEW)
        # Competitor mode
        if profile_type == SESSION_COMPETITOR_GROUP_ID:
            perms.append(PERMISSION_SESSION_VIEW)
            perms.append(PERMISSION_PROGRESS_VIEW)
            perms.append(PERMISSION_PROGRESS_MODIFY)
        return perms