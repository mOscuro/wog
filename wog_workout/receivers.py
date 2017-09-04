# """
# The receivers related to the Workout features.
# """
# from django.contrib.auth.models import Group
# from django.db.models.signals import post_save
# from django.dispatch.dispatcher import receiver
# from guardian.shortcuts import assign_perm

# from wog_workout.models import Workout




# @receiver(post_save, sender=Workout)
# def add_workout_permissions(sender, instance, **kwargs):
#     """
#     Assign admin permission to the creator of the workout.
#     If the workout is set public, add the workout to the "public workout" permission group.
#     """
#     if kwargs.get('created', True):
#         assign_perm(PERMISSION_WORKOUT_ADMIN, instance.creator, instance)
#         assign_perm(PERMISSION_WORKOUT_VIEW, instance.creator, instance)
#         assign_perm(PERMISSION_WORKOUT_MODIFY, instance.creator, instance)
#         Group.objects.create(name='Workout-%s-view' % instance.id)

#         if instance.is_public:
#             # Give view permission to all authenticated users
#             assign_perm(PERMISSION_WORKOUT_VIEW, AUTHENTICATED_USER_GROUP, instance)

