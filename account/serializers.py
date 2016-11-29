'''
Created on 28 nov. 2016

@author: Matthieu
'''
from rest_framework import serializers

from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')