from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from exercise.models import Exercise
from exercise.serializers import ExerciseSerializer
from round.helpers import create_step
from round.models import Round, Step, shift_rounds_right
from workout.models import Workout


def get_pk(context, name):
    return context['view'].kwargs.get('%s_pk' % name)

###########################################################
# WORKOUT related serializers
###########################################################
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
        fields = ('id', 'nb_repeat', 'steps')


###########################################################
# ROUND related serializers
###########################################################

def _get_default_insert_position(workout) -> int:
    return Round.objects.filter(workout=workout).count()

class RoundUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer specific to the 'update' action of a Workout.
    Can modify:
    *   name
    *   position within the Workout.
    """
    id = serializers.IntegerField(required=True)
    nb_repeat = serializers.IntegerField(required=False)
    position = serializers.IntegerField(required=False)

    class Meta:
        model = Round
        fields = ('id', 'nb_repeat', 'position')

    def validate_position(self, position: int) -> int:
        """
        Validate that the position is correct:
        *   must be a positive integer
        *   must be strictly lower than the number of TaskLists
        """
        if position is not None and position < 0:
            raise ValidationError('position must be a positive integer')
        if position >= len(Round.objects.filter(workout=self.instance.workout)):
            raise ValidationError('position cannot be bigger than the number of rounds in the workout')
        return position

    def validate_nb_repeat(self, nb_repeat: str) -> str:
        """Nb_repeat must be greater than 0"""
        if nb_repeat < 1:
            raise ValidationError('nb_repeat must be greater than 0')
        return nb_repeat

    def save(self):
        position = self.validated_data.get('position')
        if position is not None:
            self.instance.move(position)
        return super().save()


class RoundCreateSerializer(serializers.ModelSerializer):
    """
    Serializer specific to the 'create' action.
    Creation can happen at a given index (insert).
    """
    position = serializers.IntegerField(required=False)
    nb_repeat = serializers.IntegerField(required=False)

    class Meta:
        model = Round
        fields = ('nb_repeat', 'position', 'id')
        read_only_fields = ('id',)

    def validate(self, attrs):

        workout = Workout.objects.get(id=get_pk(self.context, 'workout'))
        if workout is None:
            raise ValidationError('round can only be added to an existing Workout')
        attrs['workout'] = workout
        
        # Validate the nb_repeat of the Round
        nb_repeat = attrs.get('nb_repeat', None)
        if nb_repeat is not None:
            if nb_repeat < 0:
                 raise ValidationError('Nb_repeat must be greater than 0.')

        # Validate the insert position or get the default value
        position = attrs.get('position', None)
        if position is None:
            position = _get_default_insert_position(workout)
            attrs['position'] = position
        self._validate_insertpossible(position, len(Round.objects.filter(workout=workout)))
        return super().validate(attrs)

    def _validate_insertpossible(self, position: int, max_position: int) -> None:
        """
        Validate that the position is correct, knowing:
        *   Position must be a positive integer.
        *   Position must be lower than the number of existing TaskLists.
        """
        if position is None:
            raise ValidationError('invalid position.')
        if position < 0:
            raise ValidationError('must be a positive integer.')
        if position > max_position:
            raise ValidationError('cannot be bigger than %s' % str(max_position))

    def save(self):
        position = self.validated_data['position']
        nb_repeat = self.validated_data.get('nb_repeat', 1)
        shift_rounds_right(self.validated_data['workout'], position)
        return Round.objects.create(workout=self.validated_data['workout'],
                                       nb_repeat=nb_repeat,
                                       position=position)
###########################################################
# Actions related serializers
###########################################################

class StepCreateSerializer(serializers.Serializer):
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