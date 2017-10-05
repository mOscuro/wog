from rest_framework import status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wog.mixins import ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin
from wog_round.models import Round, Step
from wog_round.serializers import RoundSerializer, RoundCreateSerializer, RoundUpdateSerializer, \
StepReadOnlySerializer, StepCreateSerializer, StepUpdateSerializer
from wog_workout import mixins as workout_mixins
from wog_workout.views import NestedInWorkoutViewSet


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
class StepInWorkoutViewSet(ListMixin, RetrieveMixin, CreateMixin,
                           UpdateMixin, DestroyMixin, NestedInWorkoutViewSet):

    queryset = Step.objects.all()
    response_serializer_class = StepReadOnlySerializer
    update_serializer_class = StepUpdateSerializer
    create_serializer_class = StepCreateSerializer

    def get_queryset(self):
        # Only the Steps within the given Round are considered
        return Step.objects.filter(round__workout=self.get_workout()).order_by('round__position', 'position')

    def list(self, request, *args, **kwargs):

        # Serialize the items and package the response
        return Response(self.get_workout_step_tree())
    
    def get_workout_step_tree(self):

        json_response = {'steps' : []}
        # get rounds for the workout
        rounds_query = Round.objects.filter(workout=self.get_workout()).order_by('position')

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

        return json_response