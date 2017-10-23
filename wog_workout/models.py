from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.db import models

from wogether.settings import AUTH_USER_MODEL
from wog_permissions.constants import (PERMISSION_SESSION_VIEW,
                                       PERMISSION_SESSION_MODIFY,
                                       PERMISSION_PROGRESS_VIEW,
                                       PERMISSION_PROGRESS_MODIFY)
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
    
    def get_step_count(self):
        count=0
        for round in self.rounds.all():
            count = count + (round.nb_repeat * round.steps.count())
        return count

    class Meta:
        unique_together = (('creator', 'name'),)
        permissions = (
            (PERMISSION_WORKOUT_VIEW, 'Can view the workout and its content'),
        )

    
class WorkoutSession(models.Model):
    """
    - A Session materialize the execution of a workout.
    - It can be seen as a pool where one or more athletes wait for the workout to start
    - A session can be planned hours or days before the beginning of the workout,
        in order to wait for other athlete than the creator to join in
    """
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='session_groups')
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='sessions')
    created_at = models.DateTimeField(auto_now=True)
    start = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        permissions = (
            (PERMISSION_SESSION_VIEW, 'Can view a workout session and its details'),
            (PERMISSION_SESSION_MODIFY, 'Can modify a workout session and its details'),
            (PERMISSION_PROGRESS_VIEW, 'Can view workout progressions'),
            (PERMISSION_PROGRESS_MODIFY, 'Can add and delete workout progressions'),
        )


class WorkoutProgression(models.Model):
    """
    - The Progression follows where an athlete is at, during a workout
    - It logs the time the athlete took to complete each step of a workout
    - The Progression will be used to update every athlete's leaderboard during a workout in "competition mode"
    """
    session = models.ForeignKey('WorkoutSession')
    step = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(AUTH_USER_MODEL)
    time = models.IntegerField() # seconds
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'session', 'step'),)
    