from rest_framework import serializers
from wog_exercise.models import Exercise, Equipment, Exercise_Type

##########################################################
# EXERCISE
##########################################################
class ExerciseSerializer(serializers.ModelSerializer):
    
    level = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
        
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'level', 'equipment', 'type', 'muscles')
    
    def get_level(self, obj):
        return obj.get_level_display()
    
    def get_type(self, obj):
        return obj.get_type_display()


##########################################################
# EQUIPMENT
##########################################################       
class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Equipment
        fields = ('id', 'name')

class ExerciseTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exercise_Type
        fields = ('name')