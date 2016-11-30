'''
Created on 28 nov. 2016

@author: Matthieu
'''
from rest_framework import serializers

#from wogether.settings import AUTH_USER_MODEL
from accounts.models import User

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'is_staff')