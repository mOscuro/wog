from django.utils.translation import ugettext_lazy as _
from django.db import models


#########
# Round #
#########
class Round(models.Model):
    """
    - A Round is a container for steps.
    It can be repeated multiple times during the execution of the Workout.    
    """
    workout = models.ForeignKey('workout.Workout', related_name='rounds', on_delete=models.CASCADE)
    nb_repeat = models.IntegerField(default=1)
    position = models.PositiveSmallIntegerField(default=0, blank=True)
   
    def __str__(self):
        return "1 round of "
        if self.nb_repeat == 1:
            return self.nb_repeat+" round of "
        else:
            return self.nb_repeat+" rounds of "

    def move(self, to_position: int) -> None:
        """Move a Round to another position within its Workout."""
        if self.position == to_position:
            # Nothing to update
            return
        if to_position < 0:
            raise ValueError('position cannot be negative')
 
        old_position = self.position
        if to_position < self.position:
            # Moving left: shift right the Rounds between to and from - 1
            shift_rounds_right(self.workout, to_position, old_position-1)
        else:
            # Moving right: shift left the Rounds between from and to
            shift_rounds_left(self.workout, old_position + 1, to_position)

        # Finally, update the position of the current Round
        self.position = to_position
        super().save()

    def delete(self, *args, **kwargs):
        """Deletes a Round."""
        # Shift the other Round left
        shift_rounds_left(workout=self.workout, from_position=self.position)

        # Actually delete the step
        return super().delete(*args, **kwargs)

def shift_rounds_right(workout, from_position: int, to_position: int=None) -> None:
    """
    Shift Rounds to the right.
    Can happen when a Round is moved or inserted.
    """
    if to_position:
        # Shift Rounds between the given two indexes
        Round.objects.filter(workout=workout,
                                position__range=(from_position, to_position))\
                        .update(position=F('position') + 1)
    else:
        # Shift all Rounds from the given index
        Round.objects.filter(workout=workout,
                                position__gte=from_position)\
                        .update(position=F('position') + 1)

def shift_rounds_left(workout, from_position: int, to_position: int=None) -> None:
    """
    Shift Rounds to the left. Can happen when a Round is moved.
    """
    # Shift Rounds between the given two indexes
    Round.objects.filter(workout=workout,
                            position__range=(from_position, to_position))\
                    .update(position=F('position') - 1)    

#########
# Steps #
#########
class Step(models.Model):
    """
    - A Step describes the smallest part of a Workout
    - Exemples :
        -- 15 pullups
        -- 10 bench press @ 15Kg
    - A Step is always linked to a Workout
    - A Step can be linked to a Round but not always
    """
    round = models.ForeignKey('Round', related_name='round_steps')
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE)
    nb_rep = models.IntegerField(default=1)
    distance = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    rest_time = models.IntegerField(default=0)
    position = models.PositiveSmallIntegerField(default=0, blank=True)
    
    #class Meta:
        #unique_together = ('workout', 'numero')
    
    def __str__(self):
        return str(self.nb_rep) + " " + self.exercise.name


    def move(self, to_position: int) -> None:
        """Move a Step to another position within its Round."""
        if to_position < 0:
            raise ValueError('position cannot be negative')
        if self.position == to_position:
            # Nothing to update
            return
 
        if to_position < self.position:
            # Moving up: shift down the Steps in the Round where 'to <= position < from'
            shift_steps_down(
                round=self.round,
                from_position=to_position,
                to_position=self.position-1)
        else:
            # Moving down: shift up the Steps in the Round where 'from < position < to'
            shift_steps_up(
                round=self.round,
                from_position=self.position + 1,
                to_position=to_position)

        # Finally, update the position of the current Step
        self.position = to_position
        super().save()

    def move_to_round(self, new_round, to_position: int) -> None:
        """
        Change Round of a Step without taking care of position
        """
        if to_position < 0:
            raise ValueError('position cannot be negative')
        if new_round is None:
            raise ValueError('Cannot move Step to non-existing Round')
        if self.round.workout != new_round.workout:
            raise ValueError('Cannot move Step between different Workouts')

        # Change the Round
        old_round = self.round
        old_round_position = self.position
        self.round = new_round
        self.position = len(new_round.steps.all())

        # Reposition the steps in the previous Round
        shift_steps_up(
            round=old_round,
            from_position=old_round_position + 1)

        # Reposition this step and the other ones in the new Round
        shift_steps_down(
            round=self.round,
            from_position=to_position)

        self.save()

    def delete(self, *args, **kwargs):
        """Deletes a step."""
        # Shift Steps up in the Round
        shift_steps_up(round=self.round, from_position=self.position + 1)

        # Actually delete the Step
        return super().delete(*args, **kwargs)


def shift_steps_down(from_position: int, to_position: int=None, round: Round=None) -> None:
    """
    Shift Steps to the bottom. Can happen when a Step is moved or inserted.
    Params:
    -   `from_position`: the position at which to start shifting steps.
    -   `to_position`: the position of the last Step to update.
    -   `round`: Round to reorder the steps in.
    """
    if to_position is not None:
        # Shift Steps between the given two indexes
        Step.objects.filter(round=round,
                            position__range=(from_position, to_position))\
                    .update(position=F('position') + 1)
    else:
        # Shift all Steps from the given index
        Step.objects.filter(round=round,
                        position__gte=from_position)\
                .update(position=F('position') + 1)

def shift_steps_up(from_position: int, to_position: int=None, round: Round=None) -> None:
    """
    Shift Steps to the top. Can happen when a Step is moved.
    Params:
    -   `from_position`: the position at which to start shifting steps.
    -   `to_position`: the position of the last Step to update.
    -   `round`: Round to reorder the steps in.
    """
    if to_position is not None:
        # Shift Steps between the given two indexes
        Step.objects.filter(round=round,
                            position__range=(from_position, to_position))\
                    .update(position=F('position') - 1)
    else:
        # Shift all Steps from the given index
        Step.objects.filter(round=round,
                            position__gte=from_position)\
                    .update(position=F('position') - 1)
