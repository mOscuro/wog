from django.db import models

# All the data related to Exercises (Exercises, Types, Equipments, Muscles)
# will be created and handled by Administration Team Only

class Exercise(models.Model):
    """
    An Exercise can be integrated into a Wod_Step of a Workout
    but can also be executed on its own
    """
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    equipement = models.ForeignKey(Equipment)
    type = models.ForeignKey(Exercice_Type)
    muscles = models.ManyToManyField(Muscle)

    def __str__(self):
        return self.name    
    
class Exercise_Type(models.Model):
    """
    Type is used to categorize Exercises
    Can be Bodyweight, TRX, Powerlifting, Weightlifting ....
    """
    name = models.CharField(max_length=50)
    
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
    Muscles workingduring exercise
    Biceps, Quads, Abs
    """
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name