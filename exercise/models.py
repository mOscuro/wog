from django.db import models
from exercise.exercise_constants import Exercise_Level, Exercise_Type, MEDIUM, BODYWEIGHT

# All the data related to Exercises (Exercises, Types, Equipments, Muscles)
# will be created and handled by Administration Team Only

class Equipment(models.Model):
    """
    - Identifying wich equipment is required is used to 
    - Barbell, Dumbell, Bench, Pullup Bar...
    - An Muscle can only be created by an administrator
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Muscle(models.Model):
    """
    - Muscles working during exercise
    - Biceps, Quads, Abs
    - A Muscle can only be created by an administrator
    """
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Exercise(models.Model):
    """
    - An Exercise will be integrated into a Wod_Step of a Workout
    - An Exercise can only be created by an administrator
    """
    
    name = models.CharField(max_length=50)
    equipement = models.ForeignKey(Equipment, blank=True, null=True)
    level = models.IntegerField(choices=Exercise_Level, default=MEDIUM)
    type = models.IntegerField(choices=Exercise_Type, default=BODYWEIGHT)
    muscles = models.ManyToManyField(Muscle, blank=True)

    def __str__(self):
        return self.name    
    