from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status

from wog.tests import WogetherAPITestCase
from wog_workout.models import WorkoutSession
from wog_permissions.constants import SESSION_INVITED_GROUP_ID, SESSION_SPECTATOR_GROUP_ID, SESSION_COMPETITOR_GROUP_ID
from wog_permissions.helpers import get_permission_profile, update_user_session_permission


class WorkoutSessionPermissionApiDetailTestsCase(WogetherAPITestCase):
    """
    Test WorkoutSession permissions:
    Only Session creator can update or delete it, and invite other users.
    """
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
        
        # Create workout session on public workout
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



class WorkoutSessionSocialApiTestsCase(WogetherAPITestCase):

    def setUp(self):
        super().setUp()
        self.user1 = self.create_user(1)
        self.workout1 = self.create_workout(name='user1_workout1', creator=self.user1, is_public=False)
        self.session1 = self.create_session(workout=self.workout1, creator=self.user1, is_public=False)
        self.user2 = self.create_user(2)
        self.user3 = self.create_user(3)

    def test_workout_session_invite_group(self):
        # User 1 should see session
        response = get_workout_session_detail(self.client, self.workout1.id, self.session1.id, self.user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should not be able to see session
        response = get_workout_session_detail(self.client, self.workout1.id, self.session1.id, self.user2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User 2 should not be able to invite a user
        response = invite_user_on_session(self.client, self.session1, self.user3, self.user2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User 1 should be able to invite User 2
        response = invite_user_on_session(self.client, self.session1, self.user2, self.user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should now be in session invite group
        invite_permission_group = get_permission_profile(self.session1, SESSION_INVITED_GROUP_ID)
        self.assertTrue(self.user2 in invite_permission_group.users.all())

        # User 2 should now be able to see session
        response = get_workout_session_detail(self.client, self.workout1.id, self.session1.id, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should not be able to get session progressions list
        response = get_session_progression_list(self.client, self.session1.id, self.user2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User 2 should not be able to create session progressions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(get_session_progression_list_url(self.session1.id),
                                    data={"step": 0, "time": 60})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workout_session_spectator_group(self):
        """Only invited users should be able to join session spectator group."""
        # User 2 should not be able to join spectator group
        response = join_session_spectator_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User 1 invites User 2 on session
        invite_user_on_session(self.client, self.session1, self.user2, self.user1)

        # User 2 should now be able to join spectator group
        response = join_session_spectator_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should now be in session spectator group
        spectator_permission_group = get_permission_profile(self.session1, SESSION_SPECTATOR_GROUP_ID)
        self.assertTrue(self.user2 in spectator_permission_group.users.all())

        # User 2 should be able to get session progressions list
        response = get_session_progression_list(self.client, self.session1.id, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should not be able to create session progressions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(get_session_progression_list_url(self.session1.id),
                                    data={"step": 0, "time": 60})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workout_session_competitor_group(self):
        """Only invited users should be able to join session spectator group."""
        # User 2 should not be able to join competitor group
        response = join_session_competitor_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User 1 invites User 2 on session
        invite_user_on_session(self.client, self.session1, self.user2, self.user1)

        # User 2 should now be able to join spectator group
        response = join_session_competitor_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should now be in session spectator group
        competitor_permission_group = get_permission_profile(self.session1, SESSION_COMPETITOR_GROUP_ID)
        self.assertTrue(self.user2 in competitor_permission_group.users.all())

        # User 2 should be able to get session progressions list
        response = get_session_progression_list(self.client, self.session1.id, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User 2 should not be able to create session progressions
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(get_session_progression_list_url(self.session1.id),
                                    data={"step": 0, "time": 60})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_workout_session_quit_invite_group(self):
        # User 1 invites User 2 on session
        invite_user_on_session(self.client, self.session1, self.user2, self.user1)
        # Check User 2 is in group
        invite_permission_group = get_permission_profile(self.session1, SESSION_INVITED_GROUP_ID)
        self.assertTrue(self.user2 in invite_permission_group.users.all())
        # User 2 should be able to quit invite groupe
        response = quit_session_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 2 should not be in invite group anymore
        self.assertFalse(self.user2 in invite_permission_group.users.all())

    def test_workout_session_quit_spectator_group(self):
        # User 1 invites User 2 on session
        invite_user_on_session(self.client, self.session1, self.user2, self.user1)
        join_session_spectator_group(self.client, self.session1, self.user2)
        # Check User 2 is in group
        spectator_permission_group = get_permission_profile(self.session1, SESSION_SPECTATOR_GROUP_ID)
        self.assertTrue(self.user2 in spectator_permission_group.users.all())
        # User 2 should be able to quit invite groupe
        response = quit_session_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 2 should not be in invite group anymore
        self.assertFalse(self.user2 in spectator_permission_group.users.all())

    def test_workout_session_quit_competitor_group(self):
        # User 1 invites User 2 on session
        invite_user_on_session(self.client, self.session1, self.user2, self.user1)
        join_session_competitor_group(self.client, self.session1, self.user2)
        # Check User 2 is in group
        competitor_permission_group = get_permission_profile(self.session1, SESSION_COMPETITOR_GROUP_ID)
        self.assertTrue(self.user2 in competitor_permission_group.users.all())
        # User 2 should be able to quit invite groupe
        response = quit_session_group(self.client, self.session1, self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 2 should not be in invite group anymore
        self.assertFalse(self.user2 in competitor_permission_group.users.all())


####################################################
# Utilities for this file's tests
####################################################
# WORKOUT SESSION
def get_workout_session_list_url(workout_pk: int):
    return reverse('workout-sessions-list', kwargs={'workout_pk': workout_pk})

def get_workout_session_list(client, workout_pk: int, user=None):
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_session_list_url(workout_pk))

def get_workout_session_detail_url(workout_pk: int, session_pk: int):
    return reverse('workout-sessions-detail', kwargs={'workout_pk': workout_pk, 'pk': session_pk})

def get_workout_session_detail(client, workout_pk: int, session_pk: int, user=None):
    if user:
        client.force_authenticate(user=user)
    return client.get(get_workout_session_detail_url(workout_pk, session_pk))

########################################################################################
# WORKOUT PROGRESSION
def get_session_progression_list_url(session_pk: int):
    return reverse('session-progressions-list', kwargs={'session_pk': session_pk})

def get_session_progression_list(client, session_pk: int, user=None):
    if user:
        client.force_authenticate(user=user)
    return client.get(get_session_progression_list_url(session_pk))

def get_session_progression_detail_url(session_pk: int, progression_pk: int):
    return reverse('session-progressions-detail', kwargs={'session_pk': session_pk, 'pk': progression_pk})

def get_session_progression_detail(client, session_pk: int, progression_pk: int, user=None):
    if user:
        client.force_authenticate(user=user)
    return client.get(get_session_progression_detail_url(session_pk, progression_pk))

########################################################################################
def invite_user_on_session(client, session: 'Session', invite_user: 'User', user=None):
    """Send PATCH request on /workouts/{workout_pk}/sessions/{session_pk}/invite/ endpoint."""
    if user:
        client.force_authenticate(user=user)
    return client.patch('%sinvite/' % get_workout_session_detail_url(session.workout.id, session.id), data={"user": invite_user.id})

def join_session_spectator_group(client, session: 'Session', user=None):
    """Send PATCH request on /workouts/{workout_pk}/sessions/{session_pk}/watch/ endpoint."""
    if user:
        client.force_authenticate(user=user)
    return client.patch('%swatch/' % get_workout_session_detail_url(session.workout.id, session.id))

def join_session_competitor_group(client, session: 'Session', user=None):
    """Send PATCH request on /workouts/{workout_pk}/sessions/{session_pk}/compete/ endpoint."""
    if user:
        client.force_authenticate(user=user)
    return client.patch('%scompete/' % get_workout_session_detail_url(session.workout.id, session.id))

def quit_session_group(client, session: 'Session', user=None):
    """Send PATCH request on /workouts/{workout_pk}/sessions/{session_pk}/quit/ endpoint."""
    if user:
        client.force_authenticate(user=user)
    return client.patch('%squit/' % get_workout_session_detail_url(session.workout.id, session.id))
