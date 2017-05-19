from rest_framework import viewsets, permissions

from exercise.serializers import ExerciseSerializer, EquipmentSerializer
from exercise.models import Exercise, Equipment
from exercise.permissions import IsAdminOrReadOnly

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
    