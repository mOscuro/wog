"""
The receivers related to the Workout features.
"""
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from wog_workout.models import Workout



@receiver(post_save, sender=Workout)
def add_workout_permissions(sender, instance, **kwargs):
    """
    Assign admin permission to the creator of the workout.
    If the workout is set public, add the workout to the "public workout" permission group.
    """
    #if kwargs.get('created', True):
        # TODO
