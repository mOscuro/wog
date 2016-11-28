'''
Created on 28 nov. 2016

@author: Matthieu
'''

from django.db.models.signals import post_save
from account.models import Account
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=Account)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        Token.objects.create(user=instance)