from annoying.functions import get_object_or_None
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from wog_exercise.models import Exercise
from wog_exercise.serializers import ExerciseSerializer
from wog_round.helpers import create_step
from wog_round.models import Round, Step, shift_rounds_right
from wog_workout.models import Workout


def get_pk(context, name):
    return context['view'].kwargs.get('%s_pk' % name)

# TODO: Global Helper 
def _validation_error(param: str, message: str):
    """Helper: throws a ValidationError."""
    raise ValidationError('Invalid parameter "%s": %s' % (param, _(message)))

###########################################################
# WORKOUT related serializers
###########################################################
class StepReadOnlySerializer(serializers.ModelSerializer):
    """
    Retrieve the detailed informations of a step (using Exercise detail).
    Used to build the detailed of a Round model instance.
    """
    exercise = ExerciseSerializer()
    
    class Meta:
        model = Step
        fields = ('id', 'position', 'nb_rep', 'exercise', 'weight', 'distance')


class RoundSerializer(serializers.ModelSerializer):
    """
    A round is a container for steps.
    """
    steps = StepReadOnlySerializer(many=True)
    class Meta:
        model = Round 
        fields = ('id', 'position', 'nb_repeat', 'steps')


###########################################################
# ROUND related serializers
###########################################################

def _get_default_round_insert_position(workout) -> int:
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
            raise _validation_error('position', 'position must be a positive integer')
        if position >= len(Round.objects.filter(workout=self.instance.workout)):
            raise _validation_error('position', 'position cannot be bigger than the number of rounds in the workout')
        return position

    def validate_nb_repeat(self, nb_repeat: str) -> str:
        """Nb_repeat must be greater than 0"""
        if nb_repeat < 1:
            raise _validation_error('nb_repeat', 'nb_repeat must be greater than 0')
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
                 raise _validation_error('nb_repeat', 'Nb_repeat must be greater than 0.')

        # Validate the insert position or get the default value
        position = attrs.get('position', None)
        if position is None:
            position = _get_default_round_insert_position(workout)
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
            raise _validation_error('position', 'invalid position.')
        if position < 0:
            raise _validation_error('position', 'must be a positive integer.')
        if position > max_position:
            raise _validation_error('position', 'cannot be bigger than %s' % str(max_position))

    def save(self):
        position = self.validated_data['position']
        nb_repeat = self.validated_data.get('nb_repeat', 1)
        shift_rounds_right(self.validated_data['workout'], position)
        return Round.objects.create(workout=self.validated_data['workout'],
                                       nb_repeat=nb_repeat,
                                       position=position)


###########################################################
# Step related serializers
###########################################################
def _get_default_step_insert_position(round) -> int:
    return Step.objects.filter(round=round).count()

class StepCreateSerializer(serializers.Serializer):
    exercise_pk = serializers.IntegerField(required=True)
    nb_rep = serializers.IntegerField(required=True)
    weight = serializers.IntegerField(required=False)
    position = serializers.IntegerField(required=False)
    distance = serializers.IntegerField(required=False)

    def validate(self, attrs):
        # Check if workout_pk is valid
        workout = get_object_or_None(Workout, id=get_pk(self.context, 'workout'))
        if workout is None:
            raise ValidationError('A step can only be added to an existing Workout.')
        # Check if round_pk is valid
        round = get_object_or_None(Round, id=get_pk(self.context, 'round'))
        if round is None:
            raise ValidationError('A step can only be added to an existing Round.')
        attrs['round'] = round

        # Check whether user has permission to view related workout
        if not self.context['request'].user.has_perm('workout.view_workout', workout):
            raise ValidationError(_('Incorrect'))

        # Check whether user has permission to create a task within this workout
        if not self.context['request'].user.has_perm('workout.add_workout_step', workout):
            raise PermissionDenied()

        # Check if exercise_pk was provided and valid
        exercise_pk = attrs.get('exercise_pk', None)
        if exercise_pk is not None:
            exercise = get_object_or_None(Exercise, id=exercise_pk)
            attrs['exercise'] = exercise
            if exercise is None:
                raise _validation_error('exercise_pk', 'Specified Exercise not found.')

        # Retrieve the position (or fallback to default value)
        position = attrs.get('position')
        if position is None:
            position = _get_default_step_insert_position(round)
            attrs['position'] = position

        # Validate round/position
        error_message = self._validate_insertpossible(position, len(round.steps.all()))
        if error_message is not None:
            _validation_error('position', error_message)
        
        attrs['nb_rep'] = attrs.get('nb_rep', 1)
        attrs['weight'] = attrs.get('weight', 0) # TODO : Manage Kgs and Lbs
        attrs['distance'] = attrs.get('distance', 0) # TODO : Manage Kms and meters
        
        return attrs

    def _validate_insertpossible(self, position: int, max_position: int) -> str:
        """
        Validate that the position is correct, knowing:
        *   Position must be a positive integer.
        *   Position must be lower than the number of existing Tasks in the related object.
        Returns error reason if there is an error.
        """
        if position is None:
            return 'invalid position'
        if position < 0:
            return 'must be a positive integer.'
        if position > max_position:
            return 'cannot be bigger than %s' % str(max_position)

    def save(self):
        return Step.objects.create(round=self.validated_data.get('round'),
                                    position=self.validated_data.get('position'),
                                    exercise=self.validated_data.get('exercise'),
                                    nb_rep=self.validated_data.get('nb_rep', 1),
                                    distance=self.validated_data.get('distance', 0),
                                    weight=self.validated_data.get('weight', 0))


class StepUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer specific to the 'update' action of a Step.
    Can modify:
    *   round the step is in
    *   nb_rep / exercise / weight attributes
    *   position within the Round
    """
    round_pk = serializers.IntegerField(required=False)
    nb_rep = serializers.IntegerField(required=False)
    exercise_pk = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)
    position = serializers.IntegerField(required=False)

    class Meta:
        model = Step
        fields = ('round_pk', 'position', 'nb_rep', 'exercise_pk', 'weight')

    def validate(self, attrs: dict) -> dict:
        if 'round_pk' in attrs:
            # Modification may include moving to another round
            # Retrieve the Round from the ID in the URL
            round_pk = attrs.get('round_pk')
            if round_pk == self.instance.round.id:
                # Not actually a different round
                del attrs['round_pk']
                if 'position' in attrs:
                    self._validate_moveinround(attrs['position'])
            else:
                # Actually a different round
                round = get_object_or_None(Round, id=round_pk)
                if round is None:
                    _validation_error('round_pk',
                                      'a step can only be added to an existing Round')
                position = attrs.get('position')
                if position is None:
                    # No position specified, defaulting
                    position = _get_default_step_insert_position(round)
                    attrs['position'] = position
                self._validate_movetoround(round, position)
        elif 'position' in attrs:
            # Modification includes moving within the round
            self._validate_moveinround(attrs['position'])
        return attrs

    def validate_weight(self, weight: float) -> float:
        if weight < 0:
            raise ValidationError('Weight cannot be negative')
        return weight

    def validate_nb_rep(self, nb_rep: int) -> int:
        """nb_rep is a quantity and must be between greater or equal"""
        if nb_rep <= 0:
            _validation_error('nb_rep', 'must be an greater or equal to 1')
        return nb_rep

    def _validate_movetoround(self, round, position: int) -> None:
        """
        Validate that moving the Step to another Round is possible:
        *   destination round must exist
        *   the position must be a positive integer
        *   the position is <= number of items existing in the destination round
        """
        if round is None:
            _validation_error('round', 'invalid round')
        if self.instance.round.workout != round.workout:
            _validation_error('round', 'cannot move Step to a different workout')
        if position is None:
            _validation_error('position', 'invalid position')
        if position < 0:
            _validation_error('position', 'must be a positive integer.')
        if position > len(round.steps.all()):
            _validation_error('position', 'cannot be > number of steps in the round')

    def _validate_moveinround(self, position: int) -> None:
        """
        Validate that moving the Step within its current Round is possible:
        *   the position must be a positive integer
        *   the position is < number of items existing in the round
        """
        if position is None:
            _validation_error('position', 'invalid position')
        if position < 0:
            _validation_error('position', 'must be a positive integer.')
        if position >= len(self.instance.round.steps.all()):
            _validation_error('position', 'cannot be >= number of steps in the round')

    def save(self):
        # Eventually makes modifications related to round changes
        position = self.validated_data.get('position')
        round_pk = self.validated_data.get('round_pk', None)
        if round_pk is not None:
            round = get_object_or_None(Round, id=round_pk)
            self.validated_data['round'] = round
            self.instance.move_to_round(new_round=round,
                                           to_position=position)
        elif position is not None:
            self.instance.move(to_position=position)

        return super().save()