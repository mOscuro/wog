from django.db import models

from workout.models import WorkoutItemNode


class RoundManager(models.Manager):
    def create(self, *args, **kwargs):
        if kwargs.get('workout', None) is None:
            raise AttributeError(_('Workout must be provided'))

        new_round = super(RoundManager, self).create(*args, **kwargs) 
        new_round.workout.add_child(instance=WorkoutItemNode(round=new_round))
        return new_round

class Round(models.Model):
    """
    - A Round is a container for steps.
    It can be repeated multiple times during the execution of the Workout.    
    """
    nb_repeat = models.IntegerField(default=1, null=True)
    workout = models.ForeignKey('workout.Workout', related_name='rounds', on_delete=models.CASCADE)
    
    objects = RoundManager()
    
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


class StepManager(models.Manager):
    def create(self, *args, **kwargs):
        
        workout_positioning = True
        round_positioning = True
        
        if kwargs.get('round', None) is None:
            round_positioning = False
            if kwargs.get('workout', None) is None:
                workout_positioning = False
                raise AttributeError(_('Either a workout or a specific round should be provided'))
            
        new_step = super(StepManager, self).create(*args, **kwargs)
#         new_step = Step(workout=kwargs['workout'], 
#                             round=kwargs.get('round', None),
#                             exercise=kwargs['exercise'],
#                             nb_rep=kwargs.get('nb_rep', 1),
#                             distance=kwargs.get('distance', 0),
#                             weight=kwargs.get('weight', 0),
#                             rest_time=kwargs.get('rest_time', 0),)
        
        if round_positioning:
            round_node = WorkoutItemNode.objects.get(round=kwargs['round'])
            round_node.add_child(instance=WorkoutItemNode(step=new_step))
        elif workout_positioning:
            kwargs['workout'].add_child(instance=WorkoutItemNode(step=new_step))

        return new_step

class Step(models.Model):
    """
    - A Step describes the smallest part of a Workout
    - Exemples :
        -- 15 pullups
        -- 10 bench press @ 15Kg
    - A Step is always linked to a Workout
    - A Step can be linked to a Round but not always
    """
    round = models.ForeignKey('Round', related_name='round_steps', null=True)
    workout = models.ForeignKey('workout.Workout', related_name='wod_step')
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE)
    nb_rep = models.IntegerField(default=1)
    distance = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    rest_time = models.IntegerField(default=0)
    
    objects = StepManager()
    #class Meta:
        #unique_together = ('workout', 'numero')
    
    def __str__(self):
        return str(self.nb_rep) + " " + self.exercise.name   