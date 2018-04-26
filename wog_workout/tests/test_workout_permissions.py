from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status

from wog.management.commands.create_permissions import create_permissions
from wog.tests import WogetherAPITestCase, WogetherTestCase
from wog_exercise.exercise_constants import AMATEUR, BODYWEIGHT
from wog_exercise.models import Exercise
from wog_workout.constants import PERMISSION_WORKOUT_VIEW, PERMISSION_WORKOUT_MODIFY
from wog_user.models import User
from wog_workout.models import Workout


class WorkoutPermissionsTestCase(TestCase):
    def setUp(self):
        create_permissions()
        
        self.user1 =  User.objects.create_user(email="user1d@wogether.com", username="user1", password="Password44$")
        self.user2 =  User.objects.create_user(email="user2d@wogether.com", username="user2", password="Password44$")

        #TODO: move setup in more generic TestCase
        burpees = Exercise.objects.create(name="Burpees", level=AMATEUR, type=BODYWEIGHT)
        self.wod_private = Workout.objects.create(name="Hundred-B", is_public=False, is_staff=False, creator=self.user1)
        self.wod_public = Workout.objects.create(name="Fifty-B", is_public=True, is_staff=False, creator=self.user1)

    def test_basic_permissions(self):
        # All users should have basic workout permissions
        self.assertTrue(self.user1.has_perm('wog_workout.add_workout'))
        self.assertTrue(self.user1.has_perm('wog_workout.view_workout'))
        self.assertTrue(self.user1.has_perm('wog_workout.change_workout'))
        self.assertTrue(self.user1.has_perm('wog_workout.delete_workout'))

        self.assertTrue(self.user2.has_perm('wog_workout.add_workout'))
        self.assertTrue(self.user2.has_perm('wog_workout.view_workout'))
        self.assertTrue(self.user2.has_perm('wog_workout.change_workout'))
        self.assertTrue(self.user2.has_perm('wog_workout.delete_workout'))

    def test_project_model_permissions(self):
        """
        Test that a user has every Workout model permission
        """
        # User 1 is creator of workouts 1 so he has full permissions on his own workouts
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_private), "Model view permission error")
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_private), "Model change permission error")
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_public), "Model view permission error")
        self.assertTrue(self.user1.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_public), "Model change permission error")

        # User 2 should never have modify permission on user1 workouts
        self.assertFalse(self.user2.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_private), "Model view permission error")
        self.assertFalse(self.user2.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_private), "Model change permission error")

        # User 2 should be able to view user 1 public workout
        self.assertTrue(self.user2.has_perm(PERMISSION_WORKOUT_VIEW, self.wod_public), "Model view permission error")
        self.assertFalse(self.user2.has_perm(PERMISSION_WORKOUT_MODIFY, self.wod_public), "Model change permission error")



class WorkoutPermissionApiDetailTestsCase(WogetherAPITestCase):

    def setUp(self):
        super().setUp()
        self.user1 = self.create_user(1)
        self.workout1 = self.create_workout(name='user1_workout1', creator=self.user1)
        self.user2 = self.create_user(2)

    def test_workout_permissions_private(self):
        self.assertFalse(self.workout1.is_public)
        
        # Create workout for User1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try accessing workout as another user
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                                        "User2 should not be able to access User1 private workout")

    def test_workout_permissions_public(self):
        self.client.force_authenticate(user=self.user1)
        
        # Set workout as public
        response = self.client.patch(get_workout_detail_url(self.workout1), data={"is_public": True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Workout.objects.get(id=self.workout1.id).is_public)

        # Try accessing workout as another user
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                                        "User2 should be able to access User1 public workout")

    def test_workout_permissions_update_private(self):
        """Update on private workout raises 404."""
        self.client.force_authenticate(user=self.user2)

        response = self.client.patch(get_workout_detail_url(self.workout1), data={"name": "new_name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.patch(get_workout_detail_url(self.workout1), data={"is_public": True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_workout_permissions_update_private(self):
        """Update on public workout raises 403 FORBIDDEN."""
        self.workout1.is_public = True
        self.workout1.save()

        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(get_workout_detail_url(self.workout1), data={"name": "new_name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workout_permissions_delete_private(self):
        """Delete on private workout raises 404."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_workout_permissions_delete_private(self):
        """Delete on public workout raises 403 FORBIDDEN."""
        self.workout1.is_public = True
        self.workout1.save()

        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


####################################################
# Utilities for this file's tests
####################################################
# WORKOUT RELATED
def get_workout_list_url():
    return reverse('workout-list')

def get_workout_list(client, user=None):
    """
    Perform a GET call to the AssignmentList API.
    If 'user' is passed, perform an authenticated call with that user.
    """
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_list_url())

def get_workout_detail_url(workout: 'Workout'):
    return reverse('workout-detail', kwargs={'pk': workout.id})

def get_workout_detail(client, workout: 'Workout', user=None):
    """
    Perform a GET call to the TaskActionDetail API.
    If 'user' is passed, perform an authenticated call with that user.
    """
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_detail_url(workout))

# WORKOUT SESSION RELATED
def get_workout_session_list_url(workout_pk):
    return reverse('workout-sessions-list', kwargs={'workout_pk': workout_pk})

def get_workout_session_list(client, user=None):
    """
    Perform a GET call to the AssignmentList API.
    If 'user' is passed, perform an authenticated call with that user.
    """
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_list_url())
        