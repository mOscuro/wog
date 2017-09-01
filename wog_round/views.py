from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wog.mixins import ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin
from wog_round.models import Round, Step
from wog_round.serializers import RoundSerializer, RoundCreateSerializer, RoundUpdateSerializer, \
StepReadOnlySerializer, StepCreateSerializer, StepUpdateSerializer
from wog_workout import mixins as workout_mixins
from wog_workout.permissions import RoundObjectPermissions, StepObjectPermissions
from wog_workout.views import GenericWorkoutPermissionViewSet, NestedInWorkoutViewSet


####################################################
# ROUNDS
####################################################
class RoundInWorkoutViewSet(ListMixin, RetrieveMixin,
                            UpdateMixin, DestroyMixin,
                            CreateMixin, NestedInWorkoutViewSet):
    
    """[API] Rounds - All operations."""
    queryset = Round.objects.all()
    response_serializer_class = RoundSerializer
    update_serializer_class = RoundUpdateSerializer
    create_serializer_class = RoundCreateSerializer

    def get_queryset(self):
        return self.filter_on_workout(self.queryset).order_by('position')


####################################################
# STEPS
####################################################
class StepsInWorkoutView(APIView):
    """
    This special view shows all the steps of a workout.
    It takes account of number times a round can be repeated.
    """
    
    object_permission_class = RoundObjectPermissions
    
    def get(self, request, *args, **kwargs):

        if 'workout_pk' in self.kwargs:
            json_response = {'steps' : []}
            # get rounds for the workout
            rounds_query = Round.objects.filter(workout=self.kwargs['workout_pk']).order_by('position')

            nb_round = 1
            nb_step = 1
            for round in rounds_query:
                # round can be repeated multiple times
                for i in range(0, round.nb_repeat):

                    # Loop through each step of each rounds
                    for step in round.steps.all():
                        json_step = {}
                        json_step['round_position'] = nb_round
                        json_step['step_position'] = nb_step
                        step_serializer = StepReadOnlySerializer(instance=step)
                        json_step['step'] = step_serializer.data
                                                
                        json_response['steps'].append(json_step)
                        nb_step = nb_step + 1

                    # For next round
                    nb_round = nb_round + 1

            return Response(json_response)


class StepInRoundViewSet(workout_mixins.ListNestedInWorkoutMixin,
                           workout_mixins.RetrieveNestedInWorkoutMixin,
                           workout_mixins.UpdateNestedInWorkoutMixin,
                           workout_mixins.DestroyNestedInWorkoutMixin,
                           workout_mixins.CreateNestedInWorkoutMixin,
                           GenericWorkoutPermissionViewSet):
    object_permission_class = StepObjectPermissions
    serializer_class = StepReadOnlySerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return StepUpdateSerializer
        elif self.action == 'create':
            return StepCreateSerializer
        return StepReadOnlySerializer

    def get_queryset(self):
        # Only the Steps within the given Round are considered
        if 'round_pk' in self.kwargs:
            return Step.objects.filter(round=self.kwargs['round_pk'])\
                               .order_by('position')
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        step = self.get_object()
        self.check_specific_permissions(step.round.workout)
        serializer = self.get_serializer(step)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.check_specific_permissions(instance.round.workout)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = self.get_response_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # TODO: delete dependencies
        self.check_specific_permissions(instance.round.workout)
        instance.delete()
