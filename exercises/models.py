from django.db import models
from exercises.exercise_constants import *

# All the data related to Exercises (Exercises, Types, Equipments, Muscles)
# will be created and handled by Administration Team Only

class Exercise(models.Model):
    """
    An Exercise will be integrated into a Wod_Step of a Workout
    """
    
    name = models.CharField(max_length=50)
    equipement = models.ForeignKey('exercises.Equipment', blank=True, null=True)
    level = models.IntegerField(choices=Exercise_Level, default=MEDIUM)
    type = models.IntegerField(choices=Exercise_Type, default=BODYWEIGHT)
    muscles = models.ManyToManyField('exercises.Muscle', blank=True)

    def __str__(self):
        return self.name    
    
class Equipment(models.Model):
    """
    Identifying wich equipment is required is used to 
    Barbell, Dumbell, Bench, Pullup Bar...
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Muscle(models.Model):
    """
    Muscles working during exercise
    Biceps, Quads, Abs
    """
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name