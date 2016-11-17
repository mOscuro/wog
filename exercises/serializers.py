from rest_framework import serializers
from exercises.models import Exercise, Equipment, Exercise_Type

class ExerciseSerializer(serializers.Serializer):
    
    class Meta:
        model = Exercise
        fields = ('name', 'level', 'equipment', 'type', 'muscles')
        
class EquipmentSerializer(serializers.Serializer):
    
    class Meta:
        model = Equipment
        fields = ('name')

class ExerciseTypeSerializer(serializers.Serializer):
    
    class Meta:
        model = Exercise_Type
        fields = ('name')