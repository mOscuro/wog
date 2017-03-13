from rest_framework import viewsets, permissions

from exercise.serializers import ExerciseSerializer
from exercise.models import Exercise
from exercise.permissions import IsAdminOrReadOnly

# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
    