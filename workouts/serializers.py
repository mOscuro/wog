from rest_framework import serializers
from workouts.models import Workout, Step
from exercises.serializers import ExerciseSerializer


class WorkoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator')

    def get_type(self,obj):
        return obj.get_type_display()

class WorkoutListSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Workout
        fields = ('name', 'url')
        
class StepSerializer(serializers.ModelSerializer):
    
    exercise = ExerciseSerializer()
    
    class Meta:
        model = Step
        fields = ('round', 'numero', 'nb_rep', 'exercise', 'weight')

class WorkoutDetailSerializer(serializers.ModelSerializer):
    
    steps = StepSerializer(many=True)
    type = serializers.SerializerMethodField()
        
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator', 'steps')

    def get_type(self,obj):
        return obj.get_type_display()
