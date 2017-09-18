from django.test import TestCase
from wog.management.commands.create_permissions import create_permissions
from wog_exercise.exercise_constants import AMATEUR, BODYWEIGHT
from wog_exercise.models import Exercise
from wog_permission.constants import (PERMISSION_WORKOUT_ADMIN,
                                      PERMISSION_WORKOUT_VIEW,
                                      PERMISSION_WORKOUT_MODIFY)
from wog_user.models import User
from wog_workout.models import Workout

class WorkoutPermissionsTestCase(TestCase):
    def setUp(self):
        create_permissions()
        
        self.user1 =  User.objects.create_user(email="user1d@wogether.com",
                                               username="user1",
                                               password="Password44$")

        #TODO: move setup in more generic TestCase
        burpees = Exercise.objects.create(name="Burpees", level=AMATEUR, type=BODYWEIGHT)
        self.wod_private = Workout.objects.create(name="Hundred-B", is_public=False, is_staff=False, creator=self.user1)
        self.wod_public = Workout.objects.create(name="Fifty-B", is_public=True, is_staff=False, creator=self.user1)

    def test_basic_permissions(self):
        self.assertTrue(self.user1.has_perm('wog_workout.add_workout'))
        self.assertTrue(self.user1.has_perm('wog_workout.change_workout'))
        self.assertTrue(self.user1.has_perm('wog_workout.delete_workout'))

    def test_project_model_permissions(self):
        """
        Test that a user has every Project model permission
        """
        # User 1 is creator of workouts 1 so he has full permissions
        ### Workout 1
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_private), "Model view permission error")
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_private), "Model change permission error")
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_ADMIN, self.wod_private), "Model delete permission error")
        ### Workout 2
        self.assertFalse(self.user1.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_public), "Model view permission error")
        self.assertFalse(self.user1.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_public), "Model change permission error")
        self.assertFalse(self.user1.has_perm(PERMISSION_WORKOUT_ADMIN, self.wod_public), "Model delete permission error")