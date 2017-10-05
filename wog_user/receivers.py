"""
The receivers related to the UserAccount features.
"""
from django.contrib.auth.models import Group
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from wog_user.models import User
from wog_workout.constants import WOG_USER_GROUP_NAME

######################################
# AT USER CREATION
######################################
@receiver(post_save, sender=User)
def add_user_to_public_group(sender, instance, **kwargs):
    if kwargs.get('created', True):
        instance.groups.add(Group.objects.get(name=WOG_USER_GROUP_NAME))


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    #user = User.objects.get(email=email_address.email)
    user = email_address.user
    user.is_active = True

    user.save()