from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status

from wog.tests import WogetherAPITestCase
from wog_workout.models import WorkoutSession
from wog_permissions.constants import SESSION_INVITED_GROUP_ID
from wog_permissions.helpers import update_user_session_permission


class WorkoutPermissionApiDetailTestsCase(WogetherAPITestCase):

    def setUp(self):
        super().setUp()
        self.user1 = self.create_user(1)
        self.workout1 = self.create_workout(name='user1_workout1', creator=self.user1)
        self.user2 = self.create_user(2)

    def test_workout_session_permissions_private_workout(self):
        """Create workout session on a private workout is only possible for creator."""
        self.assertFalse(self.workout1.is_public)
        
        # Create workout session on private workout
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(get_workout_session_list_url(self.workout1.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try as another user
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(get_workout_session_list_url(self.workout1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workout_session_permissions_public_workout(self):
        """Any user should be able to create workout session on a public workout."""
        self.workout1.is_public = True
        self.workout1.save()
        
        # Create workout session on private workout
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(get_workout_session_list_url(self.workout1.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try as another user
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(get_workout_session_list_url(self.workout1.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_workout_session_permissions_update(self):
        """Only session creator can update or delete it"""
        self.workout1.is_public = True
        self.workout1.save()
        
        self.client.force_authenticate(user=self.user1)
        self.client.post(get_workout_session_list_url(self.workout1.id))
        new_session = WorkoutSession.objects.filter(workout=self.workout1).latest('id')
        
        # invite User2 to session
        update_user_session_permission(self.user2, new_session, SESSION_INVITED_GROUP_ID)

        # User2 should not be able to update User1 session
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(get_workout_session_detail_url(self.workout1.id, new_session.id),
                                        data={"start": "2017-10-01T19:00"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User2 should not be able to delete User1 session
        response = self.client.delete(get_workout_session_detail_url(self.workout1.id, new_session.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # User 1 should be able to update its session
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(get_workout_session_detail_url(self.workout1.id, new_session.id),
                                        data={"start": "2017-10-01T19:00"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 1 should be able to delete its session
        response = self.client.delete(get_workout_session_detail_url(self.workout1.id, new_session.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




####################################################
# Utilities for this file's tests
####################################################

def get_workout_session_list_url(workout_pk: int):
    return reverse('workout-sessions-list', kwargs={'workout_pk': workout_pk})

def get_workout_session_list(client, workout_pk: int, user=None):
    """
    Perform a GET call to the AssignmentList API.
    If 'user' is passed, perform an authenticated call with that user.
    """
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_session_list_url(workout_pk))

def get_workout_session_detail_url(workout_pk: int, session_pk: int):
    print(reverse('workout-sessions-detail', kwargs={'workout_pk': workout_pk, 'pk': session_pk}))
    return reverse('workout-sessions-detail', kwargs={'workout_pk': workout_pk, 'pk': session_pk})

def get_workout_session_detail(client, workout_pk: int, session_pk: int, user=None):
    """
    Perform a GET call to the AssignmentList API.
    If 'user' is passed, perform an authenticated call with that user.
    """
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_session_detail_url(workout_pk, session_pk))
        