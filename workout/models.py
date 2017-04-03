from django.utils.translation import ugettext_lazy as _
from django.db import models

from wogether.settings import AUTH_USER_MODEL
from workout.constants import Workout_Type, PRIVATE
from workout_tree.models import WorkoutTreeItem


class WorkoutManager(models.Manager):
    def create(self, *args, **kwargs):
        
        if kwargs.get('name', None) is None:
            raise AttributeError(_('Workout name is mandatory'))

#         new_workout = Workout.objects.create(name=kwargs.get('name'),
#                                              type=kwargs.get('type'),
#                                              creator=kwargs.get('creator'))
        
        new_workout = super(WorkoutManager, self).create(*args, **kwargs)
#         workout_tree_item = WorkoutTreeItem(workout=new_workout)        
#         workout_tree_item.add_root()
        WorkoutTreeItem.add_root(workout=new_workout)    
        
        
        return new_workout

class Workout(models.Model):
   
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=Workout_Type, default=PRIVATE)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='workouts')
    amrap = models.IntegerField(default=0)
    emom = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    objects = WorkoutManager()

    def __str__(self):
        return self.name
    
    def is_amrap(self):
        """
        * Workout type : As Many Reps As Possible in the given time
        """
        return self.amrap > 0

    def is_emom(self):
        """
        * Workout type : Every minute on the minute for a specified number of minutes
        """
        return self.emom > 0
    
    def has_tree_problems(self):
        problems = self.find_problems()
        return (sum([len(problems[i]) for i in range(len(problems))]) != 0)
    
    class Meta:
        unique_together = (('creator', 'name'),)
        permissions = (
            ('view_workout', 'Can view the Workout'),
            
            ('view_workout_step', 'View create a step on a Workout'),
            ('add_workout_step', 'Can create a step on a Workout'),
            ('change_workout_step', 'Can update a step on a Workout'),
            ('delete_workout_step', 'Can delete a step on a Workout'),
            
            ('view_workout_round', 'View create a round on a Workout'),
            ('add_workout_round', 'Can create a round on a Workout'),
            ('change_workout_round', 'Can update a round on a Workout'),
            ('delete_workout_round', 'Can delete a round on a Workout'),
        )

    
class Session(models.Model):
    """
    - A Session materialize the execution of a workout.
    - It can be seen as a pool where one or more athletes wait for the workout to start
    - A session can be planned hours or days before the beginning of the workout,
        in order to wait for other athlete than the creator to join in
    """
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='sessions')
    date = models.DateTimeField()
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name='athletes')
    
class Progression(models.Model):
    """
    - The Progression follows where an athlete is at, during a workout
    - It logs the time the athlete took to complete each step of a workout
    - The Progression will be used to update every athlete's leaderboard during a workout in "competition mode"
    """
    session = models.ForeignKey('Session')
    step = models.ForeignKey('round.Step')
    user = models.ForeignKey(AUTH_USER_MODEL)
    time = models.IntegerField() # seconds
    