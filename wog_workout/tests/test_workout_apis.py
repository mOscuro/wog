import pytz
from datetime import datetime, date
from django.core.urlresolvers import reverse
from rest_framework import status

from wog.tests import WogetherAPITestCase, WogetherTestCase
from wog_workout.models import Workout

class WorkoutBaseApiTestsCase(WogetherAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.user1 = self.create_user(1)
        self.workout1 = self.create_workout(name='user1_workout1', creator=self.user1)


class TaskActionApiListTestsCase(WorkoutBaseApiTestsCase):

    def setUp(self):
        super().setUp()

    # def __get_task_action_list_tests(self, response_data):
    #     # Check structure of response serializer
    #     # TODO: Fix issue with 1st level is camelCase formated but not 2nd
    #     action = response_data[0]
    #     self.assertIsNotNone(action)
    #     self.assertEqual(len(action), 9,
    #                      'Each action returned by the /projects/{project_pk}/tasks/{task_pk}/actions/ API should have 9 fields.')
    #     self.assertTrue('id' in action, 'Assignment does not contain the ''id'' field.')
    #     self.assertTrue('member' in action, 'Assignment does not contain the ''member'' field.')
    #     self.assertTrue('name' in action, 'Assignment does not contain the ''name'' field.')
    #     self.assertTrue('done' in action, 'Assignment does not contain the ''done'' field.')
    #     self.assertTrue('start' in action, 'Assignment does not contain the ''start'' field.')
    #     self.assertTrue('finish' in action, 'Assignment does not contain the ''finish'' field.')
    #     self.assertTrue('length' in action, 'Assignment does not contain the ''length'' field.')
    #     self.assertTrue('unit' in action, 'Assignment does not contain the ''unit'' field.')
    #     self.assertTrue('planningMode' in action, 'Assignment does not contain the ''planning_mode'' field.')

    def test_workout_api_list_options(self):
        """ WorkoutList API should not support OPTIONS."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.options(get_workout_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workout_api_list_put(self):
        """ WorkoutList API should not support PUT (GET and POST only)."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(get_workout_list_url(),
                                    data={'name': 'new_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "WorkoutList API should not support PUT (GET and POST only).")

    def test_workout_api_list_patch(self):
        """ WorkoutList API should not support PATCH (GET and POST only)."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(get_workout_list_url(),
                                    data={"name": "new_name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "WorkoutList API should not support PATCH (GET and POST only).")

    def test_workout_api_list_delete(self):
        """ WorkoutList API should not support DELETE (GET and POST only)."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(get_workout_list_url())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "WorkoutList API should not support DELETE (GET and POST only).")

    def test_workout_api_list(self):
        """User should be able to list workouts"""
        response = get_workout_list(self.client, self.user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.__get_workout_list_tests(response.data)

    def test_workout_api_list_post(self):
        """ WorkoutList API should support POST."""
        self.client.force_authenticate(user=self.user1)
        workout_count = Workout.objects.all().count()
        response = self.client.post(get_workout_list_url(),
                                    data={"name": "new_workout"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         "WorkoutList API should support POST.")
        self.assertEqual(Workout.objects.all().count(), workout_count + 1)


class WorkoutApiDetailTestsCase(WorkoutBaseApiTestsCase):

    def setUp(self):
        super().setUp()

    def test_workout_api_detail_options(self):
        """ WorkoutDetail API should not support OPTIONS."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.options(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workout_api_detail_put(self):
        """ WorkoutDetail API should not support PUT."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(get_workout_detail_url(self.workout1),
                                    data={'name': 'new_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "WorkoutDetail API should not support PUT.")

    def test_workout_api_detail_patch(self):
        """ WorkoutDetail API should support PATCH."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(get_workout_detail_url(self.workout1),
                                    data={"name": "new_name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, "WorkoutDetail API should support PATCH.")

    def test_workout_api_detail_delete(self):
        """ WorkoutDetail API should support DELETE."""
        self.client.force_authenticate(user=self.user1)
        workout_count = Workout.objects.all().count()
        response = self.client.delete(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         "WorkoutDetail API should support DELETE.")
        self.assertEqual(Workout.objects.all().count(), workout_count - 1)

    def test_workout_api_detail(self):
        """ WorkoutDetail API should support GET."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(get_workout_detail_url(self.workout1))
        self.assertEqual(response.status_code, status.HTTP_200_OK, "WorkoutDetail API should support GET.")

    def test_workout_api_detail_post(self):
        """ WorkoutDetail API should not support POST."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(get_workout_detail_url(self.workout1),
                                    data={"name": "task_action2"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         "WorkoutDetail API should not support POST.")

    def test_workout_api_detail_post_same_name(self):
        """Not possible for a user to create 2 workouts with same name."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(get_workout_detail_url(self.workout1),
                                    data={"name": self.workout1.name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         "Not possible for a user to create 2 workouts with same name.")

####################################################
# Utilities for this file's tests
####################################################
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

# def get_task_action_change_start_url(task_action: 'TaskAction'):
#     return '%sstart/' % (get_task_action_detail_url(task_action))

# def get_task_action_change_finish_url(task_action: 'TaskAction'):
#     return '%sfinish/' % (get_task_action_detail_url(task_action))

# def get_task_action_change_length_url(task_action: 'TaskAction'):
#     return '%sduration/' % (get_task_action_detail_url(task_action))

# # 3 helpers to change start, finish or length values in on line of code
# def set_task_action_start(client, task_action: 'TaskAction', start: str, user=None):
#     if user:
#         client.force_authenticate(user=user)
#     return client.patch(get_task_action_change_start_url(task_action),
#                              data={"date": start, "offset": 0}, format='json')

# def set_task_action_finish(client, task_action: 'TaskAction', finish: str, user=None):
#     if user:
#         client.force_authenticate(user=user)
#     return client.patch(get_task_action_change_finish_url(task_action),
#                              data={"date": finish, "offset": 0}, format='json')

# def set_task_action_length(client, task_action: 'TaskAction', length: int, user=None):
#     if user:
#         client.force_authenticate(user=user)
#     return client.patch(get_task_action_change_length_url(task_action),
#                              data={"length": length}, format='json')

# # Moves a Task from 1 date to another
# def move_task(client, task: 'Task', date: str, user: 'User'):
#     task_url = reverse('project-tasks-detail', kwargs={"project_pk": obfuscate_id(task.tasklist.project_id),
#                                               "pk": obfuscate_id(task.id)})
#     task_url = '%stimeblock' % task_url
#     if user:
#         client.force_authenticate(user=user)
#     return client.patch(task_url, data={"date": date}, format='json')