from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404

from round.models import Step
from workout.constants import STAFF, PUBLIC
from workout.models import Workout, WorkoutTree
from workout.permissions import IsCreatorOrReadOnly, IsWorkoutCreatorOrReadOnly
from workout.serializers import WorkoutDetailSerializer, StepSerializer, \
    WorkoutListSerializer, WorkoutSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    - API view to get the list of the workout
        -- ADMIN user get to see all the workout
        -- Standard user get to see his workout, staff workout, and public workout created by other users
    - Permissions:
        -- Must be authenticated to see any workout
        -- Must be the creator to update or delete a workout
    - Query parameters :
        -- perso : if equals 1, get only workout with logged in user as the creator 
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutListSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('type', 'creator',)
    
    def get_queryset(self):
        queryset = Workout.objects.all()
        user = self.request.user
        
        # Only ADMIN users can see all the workout
        if not user.is_staff:
            queryset = queryset.filter(Q(creator=user.id) | Q(type=STAFF) | Q(type=PUBLIC))
      
        # Query parameter to get only logged user workout
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
        return Step.objects.filter(workout=self.kwargs['workout_pk'])

   
class WorkoutTreeViewSet(viewsets.ModelViewSet):
    """
    API viewset used to display task lists for a given `project` (list, retrieve)
    """
    serializer_class = WorkoutTreeDetailSerializer
    #object_permission_class = ProjectObjectPermissions
    def get_queryset(self):
        return WorkoutTree.objects.filter(workout=self.kwargs['workout_pk'])
    