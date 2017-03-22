from django.db import models
from treebeard.mp_tree import MP_NodeManager

from workout.models import WorkoutTree

    
class RoundManager(MP_NodeManager):
    def create(self, *args, **kwargs):
        if kwargs.get('_workout', None) is None:
            raise AttributeError(_('Workout must be provided'))

        new_round = Round(_workout=kwargs['_workout'],
                          nb_repeat=kwargs['nb_repeat']) 
        
        kwargs['_workout'].add_child(instance=new_round)
        return new_round

class Round(WorkoutTree):
    """
    - A Round is a container for steps.
    It can be repeated multiple times during the execution of the Workout.    
    """
    _workout = models.ForeignKey('workout.Workout', related_name='rounds', on_delete=models.CASCADE)
    nb_repeat = models.IntegerField(default=1)
    
    objects = RoundManager()
    
    def get_workout(self):
        return self._workout
    
    def has_tree_problems(self):
        problems = self.find_problems()
        print(problems)
        return (sum([len(problems[i]) for i in range(len(problems))]) != 0)
    
    def __str__(self):
        return "1 round of "
        if self.nb_repeat == 1:
            return self.nb_repeat+" round of "
        else:
            return self.nb_repeat+" rounds of "
    
    
class StepManager(MP_NodeManager):
    def create(self, *args, **kwargs):
        
        workout_positioning = True
        round_positioning = True
        
        if kwargs.get('_round', None) is None:
            round_positioning = False
            if kwargs.get('_workout', None) is None:
                workout_positioning = False
                raise AttributeError(_('Either a workout or a specific round should be provided'))
        
        new_step = Step(_workout=kwargs['_workout'],
                        _round=kwargs['_round'],
                        exercise=kwargs['exercise'],
                        nb_rep=kwargs['nb_rep'],
                        distance=kwargs['distance'])        
        
        if round_positioning:
            kwargs['_round'].add_child(instance=new_step)
        elif workout_positioning:
            kwargs['_workout'].add_child(instance=new_step)

        return new_step


class Step(WorkoutTree):
    """
    - A Step describes the smallest part of a Workout
    - Exemples :
        -- 15 pullups
        -- 10 bench press @ 15Kg
    - A Step is always linked to a Workout
    - A Step can be linked to a Round but not always
    """
    _workout = models.ForeignKey('workout.Workout', related_name='wod_step')
    _round = models.ForeignKey('Round', related_name='round_steps', null=True)
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE)
    nb_rep = models.IntegerField(default=1)
    distance = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    rest_time = models.IntegerField(default=0)
    
    objects = StepManager()
    #class Meta:
        #unique_together = ('workout', 'numero')
    
    def get_workout(self):
        return self._workout
    
    def get_round(self):
        return self._round
    
    def __str__(self):
        return str(self.nb_rep) + " " + self.exercise.name   