"""
The receivers related to the UserAccount features.
"""
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from user_account.models import User


@receiver(post_save, sender=User)
def add_user_to_public_group(sender, instance, **kwargs):
    """
    Assign user to specific workout permission group at creation
    """
    #if kwargs.get('created', True):
        # TODO


#=====================================================

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    #user = User.objects.get(email=email_address.email)
    user = email_address.user
    user.is_active = True

    user.save()