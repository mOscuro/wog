# -*- coding: utf-8 -*-
"""
Define constants on Permissions for the whole Wogether project:
- permission names that can be used as Group names
- profile_type identifiers (aka PERMISSION_ID)

/!\ Modify the string constants or the private methods at your own risks
They define values in the Meta of the Models (requires migrations)
"""

 # Very global group for our users
WOG_USER_GROUP_NAME = 'wog_users'


# These are the Project permissions that can:
# - be checked manually
#       `user.has_perm(PERMISSION_PROJECT_perm, project)`
# - assigned to groups on a project instance
#       `assign_perm(PERMISSION_PROJECT_perm, group, project)`
# We do not assign permissions on Projects to users directly
# all the permission logic is handled by Groups
# see bb_permissions.models.ProjectPermissionGroup for more info
PERMISSION_WORKOUT_VIEW = 'view_workout'
PERMISSION_WORKOUT_MODIFY = 'modify_workout'
