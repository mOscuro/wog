from rest_framework import viewsets, mixins, permissions

from workouts.serializers import WorkoutDetailSerializer, StepSerializer,\
    WorkoutListSerializer, WorkoutSerializer
from workouts.models import Workout, Step
from rest_framework.generics import get_object_or_404

class StepViewSet(viewsets.ModelViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (permissions.IsAuthenticated,)

class WorkoutViewSet(viewsets.ModelViewSet):
    
    queryset = Workout.objects.all()
    serializer_class = WorkoutListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'destroy']:
            return WorkoutDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WorkoutSerializer
        return WorkoutListSerializer
    
class StepNestedInWorkoutViewSet(mixins.RetrieveModelMixin,
                                            mixins.CreateModelMixin,
                                            mixins.DestroyModelMixin,
                                            mixins.ListModelMixin,
                                            mixins.UpdateModelMixin,
                                            viewsets.GenericViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer

    #===========================================================================
    # def get_serializer_class(self):
    #     if self.action in ['update', 'partial_update']:
    #         return MemberDocumentUpdateSerializer
    #     elif self.action == 'create':
    #         return MemberDocumentCreateSerializer
    #     else:  # ['retrieve', 'list']
    #         return MemberDocumentSerializer
    #===========================================================================

    def get_workout(self, workout_pk=None):

        workout = get_object_or_404(Workout.objects.all(), pk=workout_pk)
        return workout

    def get_queryset(self):
        return Step.objects.filter(workout=self.kwargs['workout_pk'])
    