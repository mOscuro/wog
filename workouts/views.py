from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from workouts.serializers import WorkoutDetailSerializer, StepSerializer,\
    WorkoutListSerializer, WorkoutSerializer
from workouts.models import Workout, Step
from workouts.permissions import IsCreatorOrReadOnly, IsWorkoutCreatorOrReadOnly

#===============================================================================
# class StepViewSet(viewsets.ModelViewSet):
#     queryset = Step.objects.all()
#     serializer_class = StepSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#===============================================================================
    
class WorkoutViewSet(viewsets.ModelViewSet):
    
    queryset = Workout.objects.all()
    serializer_class = WorkoutListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsCreatorOrReadOnly,)
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'destroy']:
            return WorkoutDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WorkoutSerializer
        return WorkoutListSerializer
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
class StepNestedInWorkoutViewSet(viewsets.ModelViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsWorkoutCreatorOrReadOnly,)

    def get_workout(self, workout_pk=None):

        workout = get_object_or_404(Workout.objects.all(), pk=workout_pk)
        return workout

    def get_queryset(self):
        
        queryset = Step.objects.filter(workout=self.kwargs['workout_pk'])
        
        numero = self.request.query_params.get('numero', None)
        if numero is not None:
            queryset = queryset.filter(numero=numero)        
        return queryset
    