from rest_framework import serializers

from exercise.serializers import ExerciseSerializer
from workout.models import Workout, Step, Round


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Used as a homepage for the workout
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator')

    def get_type(self,obj):
        return obj.get_type_display()


class WorkoutListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Used to display a synthetic list of workouts
    """
    class Meta:
        model = Workout
        fields = ('name', 'url')


class StepSerializer(serializers.ModelSerializer):
    """
    Retrieve the detailed informations of a step (using Exercise detail).
    Used to build the detailed of a Round model instance.
    """
    exercise = ExerciseSerializer()
    
    class Meta:
        model = Step
        fields = ('id', 'nb_rep', 'exercise', 'weight')


class RoundSerializer(serializers.ModelSerializer):
    """
    A round is a container for steps.
    """
    steps = StepSerializer(many=True)
    class Meta:
        model = Round 
        fields = ('nb_repeat', 'default', 'steps')


class WorkoutDetailSerializer(serializers.ModelSerializer):
    """
    Used to get detailed vision of a workout > rounds > steps > exercises
    """
    rounds = RoundSerializer(many=True)
    type = serializers.SerializerMethodField()
        
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator', 'rounds')

    def get_type(self,obj):
        return obj.get_type_display()
