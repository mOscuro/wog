#from django.db.models import Q
from rest_framework import mixins, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from permission.core import WorkoutObjectPermissions
from round.models import Round, Step
from round.serializers import StepSerializer
from workout.constants import STAFF, PUBLIC
from workout.models import Workout
from workout.serializers import WorkoutListSerializer, WorkoutDetailSerializer, \
WorkoutCreateSerializer, WorkoutDetailUpdateSerializer


class WorkoutViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    API viewset that allows projects to be viewed or edited.
    """
    queryset = Workout.objects.filter(is_active=True).select_related('creator')
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    object_permission_class = WorkoutObjectPermissions

    def get_serializer_class(self):
        if self.action in ['retrieve', 'destroy']:
            return WorkoutDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return WorkoutDetailUpdateSerializer
        elif self.action == 'create':
            return WorkoutCreateSerializer
        else:  # there should be only 'list' action
            return WorkoutListSerializer
    
    def get_queryset(self):
        # Checking Query Parameter in URL
        workout_type = self.request.query_params.get('type', None)
        if workout_type == 'private':
            return Workout.objects.filter(creator=self.request.user)
        elif workout_type == 'public':
            return Workout.objects.filter(type=PUBLIC)
        elif workout_type == 'staff':
            return Workout.objects.filter(type=STAFF)
        else:
            return viewsets.GenericViewSet.get_queryset(self) 
    
    def perform_create(self, serializer):
        super(WorkoutViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        super(WorkoutViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        # TODO: need to remove permissions to everyone on that project in order to trigger websocket
        super(WorkoutViewSet, self).perform_destroy(serializer)


class WorkoutDetailView(APIView):

    def get(self, request, *args, **kwargs):

        if 'workout_pk' in self.kwargs:
            json_response = {'rounds' : []}
            json_round = {}

            rounds_query = Round.objects.filter(workout=self.kwargs['workout_pk']).order_by('position')

            nb_round = 1
            for round in rounds_query:

                for i in range(0, round.nb_repeat):
                    json_round['position'] = nb_round
                    round_serializer = StepSerializer(round.steps, many=True)
                    json_round['steps'] = round_serializer.data
                    nb_round = nb_round + 1

                    json_response['rounds'].append(json_round)
                    print('------------')
                    print(json_response)

            return Response(json_response)
