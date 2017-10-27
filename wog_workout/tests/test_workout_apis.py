# import pytz
# from datetime import datetime, date
# from django.core.urlresolvers import reverse
# from rest_framework import status

# from bb.exceptions import BbValidationError
# from bb.gantt.constants import (PLANNINGMODE_FINISH, PLANNINGMODE_FINISH_LENGTH,
#                                PLANNINGMODE_START, PLANNINGMODE_START_FINISH,
#                                PLANNINGMODE_START_LENGTH, PLANNINGMODE_LENGTH)
# from bb.gantt.time import TempTimeSlot
# from bb.security.obfuscation import obfuscate_id
# from bb.tests.base import BeesbusyAPITestCase, BeesbusyTestCase
# from bb.timeblocks.models import TimeSlot
# from bb_account.account.models import Account
# from bb_account.members.models import Member
# from bb_permissions.constants import (PERMISSION_PROJECT_ADMIN,
#                                       PERMISSION_PROJECT_MODIFY)
# from bb_task.tasks.models import Task
# from bb_task.actions.models import TaskAction


# class TaskActionBaseApiTestsCase(BeesbusyAPITestCase):
    
#     def setUp(self):
#         super().setUp()
#         self.user1 = self.create_user()
#         self.account1 = Account.get_user_personal_account(self.user1)
#         self.project1 = self.create_project_on_personal_account(user=self.user1, name='project1')
#         self.member1 = Member.get_user_member(self.account1, self.user1)
#         self.tasklist1 = self.project1.tasklists.first()
#         self.task1 = Task.objects.create(name='task1', tasklist=self.tasklist1)
#         self.task_action1 = TaskAction.objects.create(task=self.task1, member=self.member1, name='task_action1')


# class TaskActionApiListTestsCase(TaskActionBaseApiTestsCase):

#     def setUp(self):
#         super().setUp()

#     def __get_task_action_list_tests(self, response_data):
#         # Check structure of response serializer
#         # TODO: Fix issue with 1st level is camelCase formated but not 2nd
#         action = response_data[0]
#         self.assertIsNotNone(action)
#         self.assertEqual(len(action), 9,
#                          'Each action returned by the /projects/{project_pk}/tasks/{task_pk}/actions/ API should have 9 fields.')
#         self.assertTrue('id' in action, 'Assignment does not contain the ''id'' field.')
#         self.assertTrue('member' in action, 'Assignment does not contain the ''member'' field.')
#         self.assertTrue('name' in action, 'Assignment does not contain the ''name'' field.')
#         self.assertTrue('done' in action, 'Assignment does not contain the ''done'' field.')
#         self.assertTrue('start' in action, 'Assignment does not contain the ''start'' field.')
#         self.assertTrue('finish' in action, 'Assignment does not contain the ''finish'' field.')
#         self.assertTrue('length' in action, 'Assignment does not contain the ''length'' field.')
#         self.assertTrue('unit' in action, 'Assignment does not contain the ''unit'' field.')
#         self.assertTrue('planningMode' in action, 'Assignment does not contain the ''planning_mode'' field.')

#     def test_task_action_api_list_options(self):
#         """ TaskActionList API should not support OPTIONS."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.options(get_task_action_list_url(self.project1.id, self.task1.id))
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_task_action_api_list_put(self):
#         """ TaskActionList API should not support PUT (GET and POST only)."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.put(get_task_action_list_url(self.project1.id, self.task1.id),
#                                     data={'name': 'new_name'}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
#                          "TaskActionList API should not support PUT (GET and POST only).")

#     def test_task_action_api_list_patch(self):
#         """ TaskActionList API should not support PATCH (GET and POST only)."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.patch(get_task_action_list_url(self.project1.id, self.task1.id),
#                                     data={"done": True}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
#                          "TaskActionList API should not support PATCH (GET and POST only).")

#     def test_task_action_api_list_delete(self):
#         """ TaskActionList API should not support DELETE (GET and POST only)."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.delete(get_task_action_list_url(self.project1.id, self.task1.id))
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
#                          "TaskActionList API should not support DELETE (GET and POST only).")

#     def test_task_action_api_list(self):
#         """User should be able to list all actions for a given task"""
#         response = get_task_action_list(self.client, self.project1.id, self.task1.id, self.user1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.__get_task_action_list_tests(response.data)

#     def test_task_action_api_list_post(self):
#         """ TaskActionList API should support POST."""
#         self.client.force_authenticate(user=self.user1)
#         action_count = TaskAction.objects.all().count()
#         response = self.client.post(get_task_action_list_url(self.project1.id, self.task1.id),
#                                     data={"member": obfuscate_id(self.member1.id),
#                                           "name": "task_action2"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED,
#                          "TaskActionList API should support POST.")
#         self.assertEqual(TaskAction.objects.all().count(), action_count + 1)

#     def test_task_action_api_list_post_no_member(self):
#         """Create task action with no member should not be possible"""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.post(get_task_action_list_url(self.project1.id, self.task1.id),
#                                     data={"name": "task_action2"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
#                          'Create task action with no member should not be possible')

#     def test_task_action_api_list_post_no_name(self):
#         """Create task action with no name should not be possible"""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.post(get_task_action_list_url(self.project1.id, self.task1.id),
#                                     data={"member": obfuscate_id(self.member1.id),}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
#                          'Create task action with no member should not be possible')


# class TaskActionApiDetailTestsCase(TaskActionBaseApiTestsCase):

#     def setUp(self):
#         super().setUp()
#         start = TempTimeSlot(date=date(2017, 10, 23), unit='d', offset=0)
#         finish = TempTimeSlot(date=date(2017, 10, 28), unit='d', offset=0)
#         self.task1.start = TimeSlot.from_temp_timeslot(start)
#         self.task1.finish = TimeSlot.from_temp_timeslot(finish)
#         self.task1.length = 5
#         self.task1.unit = 'd'
#         self.task1.save()

#     def test_task_action_api_detail_options(self):
#         """ TaskActionDetail API should not support OPTIONS."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.options(get_task_action_detail_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_task_action_api_detail_put(self):
#         """ TaskActionDetail API should not support PUT."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.put(get_task_action_detail_url(self.task_action1),
#                                     data={'name': 'new_name'}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
#                          "TaskActionDetail API should not support PUT.")

#     def test_task_action_api_detail_patch(self):
#         """ TaskActionDetail API should support PATCH."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.patch(get_task_action_detail_url(self.task_action1),
#                                     data={"done": True}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK, "TaskActionDetail API should support PATCH.")

#     def test_task_action_api_detail_delete(self):
#         """ TaskActionDetail API should support DELETE."""
#         self.client.force_authenticate(user=self.user1)
#         action_count = TaskAction.objects.all().count()
#         response = self.client.delete(get_task_action_detail_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
#                          "TaskActionDetail API should support DELETE.")
#         self.assertEqual(TaskAction.objects.all().count(), action_count - 1)

#     def test_task_action_api_detail(self):
#         """ TaskActionDetail API should support GET."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.get(get_task_action_detail_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK, "TaskActionDetail API should support GET.")

#     def test_task_action_api_detail_post(self):
#         """ TaskActionDetail API should not support POST."""
#         self.client.force_authenticate(user=self.user1)
#         response = self.client.post(get_task_action_detail_url(self.task_action1),
#                                     data={"member": obfuscate_id(self.member1.id),
#                                           "name": "task_action2"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
#                          "TaskActionDetail API should not support POST.")

#     def test_task_action_api_detail_change_start(self):
#         self.client.force_authenticate(user=self.user1)
#         response = set_task_action_start(self.client, self.task_action1, "2017-10-25", self.user1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Patch on start with finish and length None should set planning_mode to `PLANNINGMODE_START`
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertEqual(task_action.planning_mode, PLANNINGMODE_START)

#     def test_task_action_api_detail_del_start(self):
#         """Set `start` value to None via DELETE http request"""
#         # Give value for `start` attrs, to be able to test deleting it
#         self.client.force_authenticate(user=self.user1)
#         set_task_action_start(self.client, self.task_action1, "2017-10-25", self.user1)
#         response = self.client.delete(get_task_action_change_start_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # `start`, `finish` and `length` are now set to null, and so shoul be `planning_mode`
#         self.assertIsNone(TaskAction.objects.get(id=self.task_action1.id).planning_mode)

#         # Trying delete `start` already None should return 404 as we try to delete unexisting Timeslot
#         response = self.client.delete(get_task_action_change_start_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_task_action_api_detail_change_finish(self):
#         """Give value to `finish` via http request"""
#         self.client.force_authenticate(user=self.user1)
#         response = set_task_action_finish(self.client, self.task_action1, "2017-10-26", self.user1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
                
#         # Patch on finish with start and length None should set planning_mode to `PLANNINGMODE_START`
#         self.assertEqual(TaskAction.objects.get(id=self.task_action1.id).planning_mode, PLANNINGMODE_FINISH)

#     def test_task_action_api_detail_del_finish(self):
#         """Set `finish` value to None via DELETE http request"""
#         # Give value for `finish` attrs, to be able to test deleting it
#         self.client.force_authenticate(user=self.user1)
#         set_task_action_finish(self.client, self.task_action1, "2017-10-26", self.user1)
#         response = self.client.delete(get_task_action_change_finish_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # `start`, `finish` and `length` are now set to null, and so shoul be `planning_mode`
#         self.assertIsNone(TaskAction.objects.get(id=self.task_action1.id).planning_mode)

#         # Trying delete `finish` already None should return 404 as we try to delete unexisting Timeslot
#         response = self.client.delete(get_task_action_change_finish_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_task_action_api_detail_change_length(self):
#         """Patch `length` of task action with `start` and `finish` set to None is not possible"""
#         self.client.force_authenticate(user=self.user1)
#         response = set_task_action_length(self.client, self.task_action1, 1, self.user1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Patch on finish with start and length None should set planning_mode to `PLANNINGMODE_START`
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertEqual(task_action.planning_mode, PLANNINGMODE_LENGTH)

#     def test_task_action_api_detail_del_length(self):
#         """Set `length` value to None via DELETE http request"""
#         # Give value for `length` attrs, to be able to test deleting it
#         self.client.force_authenticate(user=self.user1)
#         set_task_action_length(self.client, self.task_action1, 1, self.user1)
#         response = self.client.delete(get_task_action_change_length_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # `start`, `finish` and `length` are now set to null, and so shoul be `planning_mode`
#         self.assertIsNone(TaskAction.objects.get(id=self.task_action1.id).planning_mode)

#         # Trying delete `length` already None should return 400
#         response = self.client.delete(get_task_action_change_length_url(self.task_action1))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_task_action_api_detail_start_length(self):
#         """Test `planning_mode` PLANNINGMODE_START_LENGTH"""
#         set_task_action_start(self.client, self.task_action1, "2017-10-25", self.user1)
#         set_task_action_length(self.client, self.task_action1, 2, self.user1)

#         # Check `finish` value has been set and is correct (start 25 oct for 2 days : finish should be 26 oct)
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         finish = TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 27), unit='d', offset=0))
#         self.assertEqual(task_action.planning_mode, PLANNINGMODE_START_LENGTH)
#         self.assertEqual(task_action.finish, finish)

#     def test_task_action_api_detail_finish_length(self):
#         """Test `planning_mode` PLANNINGMODE_FINISH_LENGTH"""
#         set_task_action_finish(self.client, self.task_action1, "2017-10-26", self.user1)
#         set_task_action_length(self.client, self.task_action1, 1, self.user1)

#         # Check `finish` value has been set and is correct (finish 26 oct for 1 day : start should be 25 oct)
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         start = TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 25), unit='d', offset=0))
#         self.assertEqual(task_action.planning_mode, PLANNINGMODE_FINISH_LENGTH)
#         self.assertEqual(task_action.start, start)

#     def test_task_action_api_detail_check_left_offset(self):
#         """TaskAction `left_offset` value is relative to its Task `start`"""
#         set_task_action_finish(self.client, self.task_action1, "2017-10-26", self.user1)
#         set_task_action_length(self.client, self.task_action1, 1, self.user1)
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertEqual(task_action.left_offset, 2, 
#                             'task1 is from 23 oct to 27 oct included. Action starting on 25 oct should have its `offset` set to 2.')

#     def test_task_action_api_detail_check_right_offset(self):
#         """TaskAction `right_offset` value is relative to its Task `finish`"""
#         set_task_action_start(self.client, self.task_action1, "2017-10-24", self.user1)
#         set_task_action_length(self.client, self.task_action1, 2, self.user1)
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertEqual(task_action.right_offset, 2, 
#                             'task1 is from 23 oct to 27 oct included. Action finishing on 25 oct should have its `offset` set to 2.')

#         response = self.client.delete(get_task_action_change_start_url(self.task_action1))
#         task_action = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertIsNone(task_action.left_offset, 'task1 has no `start`, task_action1 `offset` should be None.')

#     def test_task_action_api_detail_move_task(self):
#         """Move parent Task and be sure related task actions move accordingly."""
#         # Task action 1 
#         set_task_action_start(self.client, self.task_action1, "2017-10-25", self.user1)
#         set_task_action_length(self.client, self.task_action1, 2, self.user1)

#         # Create another TaskAction
#         task_action2 = TaskAction.objects.create(task=self.task1, member=self.member1, name='task_action2')
#         set_task_action_start(self.client, task_action2, "2017-10-26", self.user1)
#         set_task_action_length(self.client, task_action2, 1, self.user1)

#         # Move parent Task 1 week before
#         move_task(self.client, self.task1, "2017-10-16", self.user1)

#         # task_action1 should now start 18 oct and finish 19 oct included
#         task_action1 = TaskAction.objects.get(id=self.task_action1.id)
#         self.assertTrue(task_action1.start,
#                         TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 18), unit='d', offset=0)))
#         self.assertTrue(task_action1.finish,
#                         TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 20), unit='d', offset=0)))
#         self.assertTrue(task_action1.left_offset, 2)
#         self.assertTrue(task_action1.right_offset, 1)

#         # task_action1 should now start 19 oct and finish 20 oct not included
#         task_action2 = TaskAction.objects.get(id=task_action2.id)
#         self.assertTrue(task_action2.start,
#                         TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 19), unit='d', offset=0)))
#         self.assertTrue(task_action2.finish,
#                         TimeSlot.from_temp_timeslot(TempTimeSlot(date=date(2017, 10, 20), unit='d', offset=0)))
#         self.assertTrue(task_action2.left_offset, 3)
#         self.assertTrue(task_action2.right_offset, 1)

#     def test_task_action_create_no_admin(self):
#         """Create or update TaskAction with a member not already on the project, should only be possible for admin"""
#         self.client.force_authenticate(user=self.user1)
        
#         # Create user 2, with a linked member
#         user2 = self.create_user(2)
#         member2 = self.create_member(name='member2', account=self.account1, email='user2@beesbusy.com',
#                                           created_by=self.user1, related_user=user2,
#                                           linked_at=datetime.utcnow().replace(tzinfo=pytz.utc))

#         # Add member 2 on project 1 (member2 should not have admin permission then)
#         project_member_url = reverse('project-member-list', kwargs={'project_pk': obfuscate_id(self.project1.id)})
#         response = self.client.post(project_member_url, data={"member": obfuscate_id(member2.id)}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(user2.has_perm(PERMISSION_PROJECT_MODIFY, self.project1), "Model change permission error")
#         self.assertFalse(user2.has_perm(PERMISSION_PROJECT_ADMIN, self.project1), "Model delete permission error")

#         # User 1 is admin and should be able to assign member on a task directly
#         new_member1 = self.create_member(name='new_member1', account=self.account1, created_by=self.user1)
#         action_count = TaskAction.objects.all().count()
#         response = self.client.post(get_task_action_list_url(self.project1.id, self.task1.id),
#                                         data={"member": obfuscate_id(new_member1.id),
#                                               "name": "new_action1"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(TaskAction.objects.all().count(), action_count + 1)

#         # User 2 is not admin and should not be able to create TaskAction with a member if not already added to project
#         self.client.force_authenticate(user=user2)
#         new_member2 = self.create_member(name='new_member2', account=self.account1, created_by=self.user1)
#         action_count = TaskAction.objects.all().count()
#         response = self.client.post(get_task_action_list_url(self.project1.id, self.task1.id),
#                                         data={"member": obfuscate_id(new_member2.id),
#                                               "name": "new_action2"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(TaskAction.objects.all().count(), action_count)

#         # Same scenario if user 2 tries to patch 
#         new_action1 = TaskAction.objects.get(name='new_action1')
#         response = self.client.patch(get_task_action_detail_url(new_action1),
#                                 data={"member": obfuscate_id(new_member2.id)}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# ####################################################
# # Utilities for this file's tests
# ####################################################
# def get_task_action_list_url(project_pk: str, task_pk: str):
#     return reverse('task-actions-list', kwargs={'project_pk': obfuscate_id(project_pk), 'task_pk': obfuscate_id(task_pk)})

# def get_task_action_list(client, project_pk: str, task_pk: str, user=None):
#     """
#     Perform a GET call to the AssignmentList API.
#     If 'user' is passed, perform an authenticated call with that user.
#     """
#     if user:
#         client.force_authenticate(user=user)
#     return client.get(get_task_action_list_url(obfuscate_id(project_pk), obfuscate_id(task_pk)))

# def get_task_action_detail_url(task_action: 'TaskAction'):
#     return reverse('task-actions-detail', kwargs={'project_pk': obfuscate_id(task_action.task.tasklist.project_id),
#                                                   'task_pk': obfuscate_id(task_action.task_id),
#                                                   'pk': obfuscate_id(task_action.id)})

# def get_task_action_detail(client, task_action: 'TaskAction', user=None):
#     """
#     Perform a GET call to the TaskActionDetail API.
#     If 'user' is passed, perform an authenticated call with that user.
#     """
#     if user:
#         client.force_authenticate(user=user)
#     return client.get(get_task_action_detail_url(task_action))

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