from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from exercise.models import Exercise
from exercise.serializers import ExerciseSerializer
from round.helpers import create_step
from round.models import Round, Step
from workout.models import Workout


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
        
###########################################################
# Actions related serializers
###########################################################

class CreateStepSerializer(serializers.Serializer):
    exercise = serializers.IntegerField(required=True)
    nb_rep = serializers.IntegerField(required=True)
    round = serializers.IntegerField(required=False)

    def validate(self, attrs):
        round_id = attrs.get('round', None)
        if round_id is None:
            raise ValidationError(_('You need to specify a round'))
        else:
            try:
                attrs['round'] = Round.objects.get(id=round_id)
            except Round.DoesNotExist:
                raise ValidationError(_('Incorrect round'))

        # Check whether user has permission to view related workout
        if not self.context['request'].user.has_perm('workout.view_workout', attrs['workout']):
            raise ValidationError(_('Incorrect'))

        # Check whether user has permission to create a task within this workout
        if not self.context['request'].user.has_perm('workout.add_workout_steps', attrs['workout']):
            raise PermissionDenied()

        exercise_id = attrs.get('exercise', None)
        try:
            attrs['exercise'] = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            raise ValidationError(_('Incorrect exercise'))
        
        attrs['nb_rep'] = attrs.get('nb_rep', None)
        attrs['weight'] = attrs.get('weight', None)
        
        return attrs

    def save(self):
        return create_step(self.validated_data)