from django.db import models
from treebeard.mp_tree import MP_Node, MP_NodeManager

from wogether.settings import AUTH_USER_MODEL
from workout.constants import Workout_Type, ONESHOT


class WorkoutTree(MP_Node):
    node_order_by = None


class WorkoutManager(MP_NodeManager):
    def create(self, *args, **kwargs):
        new_workout = Workout.add_root(*args, **kwargs)
        return new_workout

class Workout(WorkoutTree):
   
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=Workout_Type, default=ONESHOT)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='workouts')
    amrap = models.IntegerField(default=0)
    emom = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
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
    