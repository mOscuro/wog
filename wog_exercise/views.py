from rest_framework import viewsets, permissions

from wog_exercise.serializers import ExerciseSerializer, EquipmentSerializer
from wog_exercise.models import Exercise, Equipment
from wog_exercise.permissions import IsAdminOrReadOnly

# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):
    """ Only Staff members (admin) can create exercises """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)


class EquipmentViewSet(viewsets.ModelViewSet):
    """ Only Staff members (admin) can create equipments """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
    