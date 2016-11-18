from rest_framework import viewsets

from workouts.serializers import WorkoutSerializer
from workouts.models import Workout

# Create your views here.
class WorkoutViewSet(viewsets.ModelViewSet):

    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    