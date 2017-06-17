#===============================================================================
# Created on 28 nov. 2016
# @author: Matthieu
#===============================================================================

from rest_framework import serializers

#from wogether.settings import AUTH_USER_MODEL
from wog_user.models import User

class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'is_staff')