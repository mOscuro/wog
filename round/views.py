from rest_framework import status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from round.models import Round, Step
from round.serializers import RoundSerializer, RoundCreateSerializer, RoundUpdateSerializer, \
StepCreateSerializer, StepReadOnlySerializer
from workout import mixins as workout_mixins
from workout.permissions import RoundObjectPermissions, StepObjectPermissions
from workout.views import GenericWorkoutPermissionViewSet


####################################################
# ROUNDS
####################################################
class RoundInWorkoutViewSet(workout_mixins.ListNestedInWorkoutMixin,
                               workout_mixins.RetrieveNestedInWorkoutMixin,
                               workout_mixins.UpdateNestedInWorkoutMixin,
                               workout_mixins.DestroyNestedInWorkoutMixin,
                               workout_mixins.CreateNestedInWorkoutMixin,
                               GenericWorkoutPermissionViewSet):
    """[API] Rounds - All operations."""
    object_permission_class = RoundObjectPermissions
    serializer_class = RoundUpdateSerializer
    response_serializer_class = RoundSerializer

    def get_serializer_class(self):
        # 'Create' action has a specific serializer
        if self.action == 'create':
            return RoundCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RoundUpdateSerializer
        return RoundSerializer

    def get_queryset(self):
        return Round.objects.filter(workout=self.kwargs['workout_pk']).order_by('position')

    def perform_update(self, serializer):
        round = self.get_object()
        self.check_specific_permissions(round.workout)
        super().perform_update(serializer)

    def perform_create(self, serializer):
        return serializer.save()


class StepsInWorkoutView(workout_mixins.ListNestedInWorkoutMixin,
                        GenericWorkoutPermissionViewSet):

    object_permission_class = RoundObjectPermissions
    
    def list(self, request, *args, **kwargs):

        if 'workout_pk' in self.kwargs:
            json_response = {'rounds' : []}
            # get rounds for the workout
            rounds_query = Round.objects.filter(workout=self.kwargs['workout_pk']).order_by('position')

            nb_round = 1
            for round in rounds_query:
                # round can be repeated multiple times
                for i in range(0, round.nb_repeat):
                    json_round = {}
                    json_round['position'] = nb_round
                    round_serializer = StepReadOnlySerializer(round.steps, many=True)
                    json_round['steps'] = round_serializer.data
                    nb_round = nb_round + 1

                    json_response['rounds'].append(json_round)

            return Response(json_response)


class StepInWorkoutViewSet(workout_mixins.ListNestedInWorkoutMixin,
                           workout_mixins.RetrieveNestedInWorkoutMixin,
                           workout_mixins.UpdateNestedInWorkoutMixin,
                           workout_mixins.DestroyNestedInWorkoutMixin,
                           workout_mixins.CreateNestedInWorkoutMixin,
                           GenericWorkoutPermissionViewSet):
    object_permission_class = StepObjectPermissions
    serializer_class = StepReadOnlySerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            pass
            #return StepUpdateSerializer
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
