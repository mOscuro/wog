from rest_framework import serializers

from exercise.serializers import ExerciseSerializer
from round.models import Round, Step


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
    round_steps = StepSerializer(many=True)
    class Meta:
        model = Round 
        fields = ('nb_repeat', 'round_steps')