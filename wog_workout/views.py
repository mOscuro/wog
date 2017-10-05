#from django.db.models import Q
from rest_framework import mixins, filters, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wog_permission.permissions import IsAuthorizedForWorkout
from wog_permission.core import IsCreatorOrReadOnly
from wog.viewsets import WogViewSet
from wog.mixins import ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin
from wog_permission.core import IsCreatorOrReadOnly
from wog_round.models import Round, Step
from wog_round.serializers import StepReadOnlySerializer
from wog_workout.models import Workout
from wog_workout.serializers import WorkoutReadOnlySerializer, WorkoutDetailSerializer, \
WorkoutCreateSerializer, WorkoutUpdateSerializer


####################################################
# WORKOUTS
####################################################
class WorkoutViewSet(WogViewSet,
                     ListMixin, RetrieveMixin,
                     CreateMixin, UpdateMixin, DestroyMixin):
    # To access the Workouts, the user must be authenticated
    # and have permissions object-level permissions
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    filter_backends = (filters.DjangoObjectPermissionsFilter,)

    update_serializer_class = WorkoutUpdateSerializer
    create_serializer_class = WorkoutCreateSerializer
    response_serializer_class = WorkoutReadOnlySerializer
    serializer_class = WorkoutReadOnlySerializer
    """
    API viewset that allows projects to be viewed or edited.
    """
    queryset = Workout.objects.filter(is_active=True).select_related('creator')
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    # object_permission_class = IsWorkoutCreatorOrReadOnly

    def get_queryset(self):
        # Checking Query Parameter in URL
        workout_type = self.request.query_params.get('type', None)
        if workout_type == 'private':
            return Workout.objects.filter(creator=self.request.user)
        elif workout_type == 'public':
            return Workout.objects.filter(is_public=True, is_staff=False)
        elif workout_type == 'staff':
            return Workout.objects.filter(is_public=True, is_staff=True)
        else:
            return viewsets.GenericViewSet.get_queryset(self) 


####################################################
class NestedInWorkoutViewSet(WogViewSet):
    """Verify that the user has access to a Workout."""
    # Perform authorization validation on the workout
    permission_classes = (IsAuthorizedForWorkout,)

    def get_workout_id(self):
        """Return the reference to the workout."""
        return self.kwargs['workout_pk']

    def get_workout(self):
        """Return the referenced workout."""
        return get_object_or_404(Workout.objects.all(), pk=self.get_workout_id())

    def filter_on_workout(self, queryset):
        return queryset.filter(workout=self.get_workout_id())




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
