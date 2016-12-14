from django.db import models
from wogether.settings import AUTH_USER_MODEL
from exercises.models import Exercise
from workouts.constants import Workout_Type, ONESHOT

class Workout(models.Model):
   
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=Workout_Type, default=ONESHOT)
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='workouts')
    amrap = models.IntegerField(default=0)
    emom = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name   
    
class Step(models.Model):
    """
    - A Step describes the smallest part of a Workout
    - Exemples :
        -- 15 pullups
        -- 10 bench press @ 15Kg
    """
    workout = models.ForeignKey(Workout, related_name='steps', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    round = models.IntegerField(default=1)
    numero = models.IntegerField(blank=True, null=True)
    nb_rep = models.IntegerField()
    weight = models.FloatField(default=0)
    rest_time = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('workout', 'numero')
        ordering = ['numero']
    
    def __str__(self):
        return self.workout.name + " - " + str(self.nb_rep) + " " + self.exercise.name   

    def save(self, *args, **kwargs):

        if not self.pk and not self.numero:
            nb_step = Step.objects.filter(workout=self.workout).count()
            self.numero=nb_step+1
        super(Step, self).save(*args, **kwargs)
    
    
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
    step = models.ForeignKey(Step)
    user = models.ForeignKey(AUTH_USER_MODEL)
    time = models.IntegerField() # seconds
    