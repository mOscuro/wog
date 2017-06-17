from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from wog_permission.constants import AUTHENTICATED_USER_GROUP


class Command(BaseCommand):
    help = 'Creates Group for authenticated user with model permission'

    def handle(self, *args, **options):
        self.create_permissions()
        self.stdout.write(self.style.SUCCESS('Group permission created'))
        
    def create_permissions(self):
        auth_group, _ = Group.objects.get_or_create(name=AUTHENTICATED_USER_GROUP)
        
        # Workout permission for authenticated users
        add_workout_permission = Permission.objects.get(codename='add_workout')
        view_workout_permission = Permission.objects.get(codename='view_workout')
        change_workout_permission = Permission.objects.get(codename='change_workout')
        delete_workout_permission = Permission.objects.get(codename='delete_workout')

        auth_group.permissions.add(add_workout_permission)
        auth_group.permissions.add(view_workout_permission)
        auth_group.permissions.add(change_workout_permission)
        auth_group.permissions.add(delete_workout_permission)

        # Steps permission
        add_workout_step_permission = Permission.objects.get(codename='add_workout_step')
        view_workout_step_permission = Permission.objects.get(codename='view_workout_step')
        change_workout_step_permission = Permission.objects.get(codename='change_workout_step')
        delete_workout_step_permission = Permission.objects.get(codename='delete_workout_step')
        
        auth_group.permissions.add(add_workout_step_permission)
        auth_group.permissions.add(view_workout_step_permission)
        auth_group.permissions.add(change_workout_step_permission)
        auth_group.permissions.add(delete_workout_step_permission)

        # Round permission
        add_workout_round_permission = Permission.objects.get(codename='add_workout_round')
        view_workout_round_permission = Permission.objects.get(codename='view_workout_round')
        change_workout_round_permission = Permission.objects.get(codename='change_workout_round')
        delete_workout_round_permission = Permission.objects.get(codename='delete_workout_round')
                
        auth_group.permissions.add(add_workout_round_permission)
        auth_group.permissions.add(view_workout_round_permission)
        auth_group.permissions.add(change_workout_round_permission)
        auth_group.permissions.add(delete_workout_round_permission)
