from rest_framework import viewsets, permissions

from exercises.serializers import ExerciseSerializer
from exercises.models import Exercise
from exercises.permissions import IsAdminOrReadOnly

# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
    