# -*- coding: utf-8 -*-
"""
Define constants on Permissions for the whole Wogether project:
- permission names that can be used as Group names
- profile_type identifiers (aka PERMISSION_ID)

/!\ Modify the string constants or the private methods at your own risks
They define values in the Meta of the Models (requires migrations)
"""

# Other Wogether-specific groups
AUTHENTICATED_USER_GROUP = 'auth'
WOG_USER_GROUP_NAME = 'bb_users' # Very global group for our users

# Permission keywords for specific actions
PERMISSION_READ = 'view'
PERMISSION_WRITE = 'modify'
PERMISSION_ADMIN = 'admin'

def _get_permission_codename(name: str, profile_type: str) -> str:
    """Return the Wogether Model permission codename."""
    return '%s_%s' % (profile_type, name)

def _get_workout_permission(profile_type: str) -> str:
    """
    Helper to retrieve the full name of an Account permission,
    based on the permission type (PERMISSION_X from bb.constants).
    """
    return _get_permission_codename('workout', profile_type)

# These are the Project permissions that can:
# - be checked manually
#       `user.has_perm(PERMISSION_PROJECT_perm, project)`
# - assigned to groups on a project instance
#       `assign_perm(PERMISSION_PROJECT_perm, group, project)`
# We do not assign permissions on Projects to users directly
# all the permission logic is handled by Groups
# see bb_permissions.models.ProjectPermissionGroup for more info
PERMISSION_WORKOUT_VIEW = _get_workout_permission(PERMISSION_READ)
PERMISSION_WORKOUT_MODIFY = _get_workout_permission(PERMISSION_WRITE)
PERMISSION_WORKOUT_ADMIN = _get_workout_permission(PERMISSION_ADMIN)
