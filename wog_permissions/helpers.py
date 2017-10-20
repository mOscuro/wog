from rest_framework.exceptions import ValidationError

from wog_permissions.models import WorkoutSessionPermissionGroup
from wog_permissions.constants import (SESSION_DEFAULT_PERMISSION_ID,
                                       SESSION_INVITED_PERMISSION_ID,
                                       SESSION_SPECTATOR_PERMISSION_ID,
                                       SESSION_COMPETITOR_PERMISSION_ID)


def get_permission_profile(session, profile_type=SESSION_DEFAULT_PERMISSION_ID):
    """
    Retrieve the permission group of a project
    corresponding to a specific `profile_type`.
    If that group doesn't exist, create it.
    """
    group, created = WorkoutSessionPermissionGroup.objects.get_or_create(
        session=session, profile_type=profile_type,
    )
    if created:
        # Make sure a new Group has its permissions set
        group.assign_perms()
    return group

def delete_user_permission(user: 'User', permission_group: WorkoutSessionPermissionGroup) -> None:
    """Remove the django object-permission from the User on the given Session."""
    if user and permission_group:
        user.groups.remove(permission_group)

def add_user_permission(user: 'User', permission_group: WorkoutSessionPermissionGroup) -> None:
    """Remove the django object-permission from the User on the given Session."""
    if user and permission_group:
        user.groups.add(permission_group)

def update_user_session_permission(
        user: 'User', session: 'Session', profile_type: int) -> None:
    """Update the WorkoutSessionPermissionGroup of a User on a specific Session."""
    permission_group = get_permission_profile(session, profile_type)

    # TODO: limit case member or project is None
    current_permission_group = user.session_permissions.filter(session=session).first()
    if current_permission_group == permission_group:
        # Nothing to do
        return
    
    if user == session.creator and current_permission_group.profile_type == SESSION_COMPETITOR_PERMISSION_ID:
        # Cannot remove session creator from Competitor group
        raise ValidationError('Cannot remove creator from competitor group')

    if permission_group is not None:
        # Add the member to the new group
        permission_group.users.add(user)
        add_user_permission(user, permission_group)
    if current_permission_group is not None:
        # Remove the member from the previous Group
        current_permission_group.users.remove(user)
        delete_user_permission(user, current_permission_group)