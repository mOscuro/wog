#from django.db.models import Q
from rest_framework import mixins, filters, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from wog_permission.core import WorkoutObjectPermissions
from wog_round.models import Round, Step
from wog_round.serializers import StepReadOnlySerializer
from wog_workout.constants import STAFF, PUBLIC
from wog_workout.models import Workout
from wog_workout.serializers import WorkoutReadOnlySerializer, WorkoutDetailSerializer, \
WorkoutCreateSerializer, WorkoutUpdateSerializer


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
            return WorkoutUpdateSerializer
        elif self.action == 'create':
            return WorkoutCreateSerializer
        else:  # there should be only 'list' action
            return WorkoutReadOnlySerializer

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

    def create(self, request, *args, **kwargs):
        # We override create method to use a custom serializer for the response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create the object (instead of preform_create method)
        saved = serializer.save()
        serializer = WorkoutReadOnlySerializer(instance=saved)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # We override update method to use a custom serializer for the response
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = WorkoutReadOnlySerializer(instance=instance)
        return Response(serializer.data)
    
    def perform_destroy(self, serializer):
        # TODO: need to remove permissions to everyone on that project in order to trigger websocket
        super(WorkoutViewSet, self).perform_destroy(serializer)


####################################################
# GENERIC 'IN WORKOUT' VIEWSETS
####################################################
class GenericWorkoutPermissionViewSet(viewsets.GenericViewSet):
    object_permission_class = None
    response_serializer_class = None

    def get_workout(self, workout_pk=None):
        """
         Look for the referenced project
         """
        # Check if the referenced project exists
        workout = get_object_or_404(Workout.objects.all(), pk=workout_pk)
        self.check_specific_permissions(workout)
        return workout

    def get_object_permission(self):
        object_permission_class = self.get_object_permission_class()
        return object_permission_class()

    def get_object_permission_class(self):
        assert self.object_permission_class is not None, (
            "'%s' should either include a `object_permission_class` attribute, "
            "or override the `get_object_permission_class()` method."
            % self.__class__.__name__
        )
        return self.object_permission_class

    def check_specific_permissions(self, workout):
        permission = self.get_object_permission()
        if not permission.has_object_permission(self.request, self, workout):
            self.permission_denied(
                self.request, message=getattr(permission, 'message', None)
            )

    def get_response_serializer(self, *args, **kwargs):
        response_serializer_class = self.get_response_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return response_serializer_class(*args, **kwargs)

    def get_response_serializer_class(self):
        return self.response_serializer_class if self.response_serializer_class\
            else self.serializer_class
