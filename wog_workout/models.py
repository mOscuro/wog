from django.utils.translation import ugettext_lazy as _
from django.db import models

from wogether.settings import AUTH_USER_MODEL
from wog_workout.constants import PERMISSION_WORKOUT_VIEW, PERMISSION_WORKOUT_MODIFY


class Workout(models.Model):
   
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='workouts')
    time_cap = models.IntegerField(default=0)
    amrap = models.IntegerField(default=0)
    emom = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def is_for_time(self):
        """ Workout type : Every minute on the minute for a specified number of minutes """
        return self.time_cap > 0
    
    def is_amrap(self):
        """ Workout type : As Many Reps As Possible in the given time """
        return self.amrap > 0

    def is_emom(self):
        """ Workout type : Every minute on the minute for a specified number of minutes """
        return self.emom > 0
    
    class Meta:
        unique_together = (('creator', 'name'),)
        permissions = (
            (PERMISSION_WORKOUT_VIEW, 'Can view the workout and its content'),
        )

    
class Session(models.Model):
    """
    - A Session materialize the execution of a workout.
    - It can be seen as a pool where one or more athletes wait for the workout to start
    - A session can be planned hours or days before the beginning of the workout,
        in order to wait for other athlete than the creator to join in
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='sessions')
    date = models.DateTimeField()
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name='athletes')


class Progression(models.Model):
    """
    - The Progression follows where an athlete is at, during a workout
    - It logs the time the athlete took to complete each step of a workout
    - The Progression will be used to update every athlete's leaderboard during a workout in "competition mode"
    """
    session = models.ForeignKey(Session)
    step = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(AUTH_USER_MODEL)
    time = models.IntegerField() # seconds

    class Meta:
        unique_together = (('user', 'session', 'step'),)    
    