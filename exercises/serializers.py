from rest_framework import serializers
from exercises.models import Exercise, Equipment, Exercise_Type

class ExerciseSerializer(serializers.ModelSerializer):
    
    level = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
        
    class Meta:
        model = Exercise
        fields = ('name', 'level', 'equipement', 'type', 'muscles')
    
    def get_level(self, obj):
        return obj.get_level_display()
    
    def get_type(self, obj):
        return obj.get_type_display()
        
class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Equipment
        fields = ('name')

class ExerciseTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exercise_Type
        fields = ('name')