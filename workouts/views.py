from rest_framework import viewsets

from workouts.serializers import WorkoutSerializer, StepSerializer
from workouts.models import Workout, Step

class StepViewSet(viewsets.ModelViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer


# Create your views here.
class WorkoutViewSet(viewsets.ModelViewSet):

    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    