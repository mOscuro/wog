from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from workouts.serializers import WorkoutDetailSerializer, StepSerializer,\
    WorkoutListSerializer, WorkoutSerializer
from workouts.models import Workout, Step
from workouts.constants import STAFF, PUBLIC
from workouts.permissions import IsCreatorOrReadOnly, IsWorkoutCreatorOrReadOnly

class WorkoutViewSet(viewsets.ModelViewSet):
    """
    - API view to get the list of the workouts
        -- ADMIN user get to see all the workouts
        -- Standard user get to see his workouts, staff workouts, and public workouts created by other users
    - Permissions:
        -- Must be authenticated to see any workout
        -- Must be the creator to update or delete a workout
    - Query parameters :
        -- perso : if equals 1, get only workouts with logged in user as the creator 
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutListSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('type', 'creator',)
    
    def get_queryset(self):
        queryset = Workout.objects.all()
        user = self.request.user
        
        # Only ADMIN users can see all the workouts
        if not user.is_staff:
            queryset = queryset.filter(Q(creator=user.id) | Q(type=STAFF) | Q(type=PUBLIC))
      
        # Query parameter to get only logged user workouts
        perso = self.request.query_params.get('perso', None)
        if perso is not None:
            queryset =  queryset.filter(creator=user)    

        return queryset
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'destroy']:
            return WorkoutDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WorkoutSerializer
        return WorkoutListSerializer
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    
class StepNestedInWorkoutViewSet(viewsets.ModelViewSet):
    """
    - API view used to display details about steps in a workout
    - Query parameters :
        -- numero = used to get detail about a specific step in a workout (going from first to last)
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsWorkoutCreatorOrReadOnly,)

    def get_workout(self, workout_pk=None):

        workout = get_object_or_404(Workout.objects.all(), pk=workout_pk)
        return workout

    def get_queryset(self):
        
        queryset = Step.objects.filter(workout=self.kwargs['workout_pk'])
        
        numero = self.request.query_params.get('numero', None)
        if numero:
            queryset = queryset.filter(numero=numero)        
        return queryset
    