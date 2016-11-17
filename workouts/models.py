from django.db import models
from django.contrib.auth import User

# Create your models here.
class Workout(models.Model):
   
    name = models.CharField(max_length=100)
    public = models.BooleanField()
    creator = models.ForeignKey('auth.User')
    
class Step(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    round = models.IntegerField()
    numero = models.IntegerField()
    nb_rep = models.IntegerField()
    weight = models.FloatField()
    
class Session(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User')
    date