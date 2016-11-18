from rest_framework import viewsets

from exercises.serializers import ExerciseSerializer
from exercises.models import Exercise

# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    