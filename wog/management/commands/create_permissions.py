from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from wog_workout.constants import WOG_USER_GROUP_NAME


def create_permissions():
    auth_group, _ = Group.objects.get_or_create(name=WOG_USER_GROUP_NAME)
    
    # Workout permission for authenticated users
    add_workout_permission = Permission.objects.get(codename='add_workout')
    view_workout_permission = Permission.objects.get(codename='view_workout')
    change_workout_permission = Permission.objects.get(codename='change_workout')
    delete_workout_permission = Permission.objects.get(codename='delete_workout')

    auth_group.permissions.add(add_workout_permission)
    auth_group.permissions.add(view_workout_permission)
    auth_group.permissions.add(change_workout_permission)
    auth_group.permissions.add(delete_workout_permission)

    # Every authenticated user should be authorized to create workout sessions
    add_session_permission = Permission.objects.get(codename='add_session')
    auth_group.permissions.add(add_session_permission)

class Command(BaseCommand):
    help = 'Creates Group for authenticated user with model permission'

    def handle(self, *args, **options):
        create_permissions()
        self.stdout.write(self.style.SUCCESS('Group permission created'))
        
