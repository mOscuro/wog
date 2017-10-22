from django.db.models.query_utils import Q
from rest_framework import mixins, filters, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wog_permissions.permissions import IsWorkoutCreatorOrReadOnly, IsSessionCreatorOrReadOnly
from wog.viewsets import WogViewSet
from wog.mixins import ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin
from wog_round.models import Round, Step
from wog_round.serializers import StepReadOnlySerializer
from wog_workout.models import Workout, WorkoutSession, WorkoutProgression
from wog_workout.serializers.workout import (WorkoutReadOnlySerializer, WorkoutDetailSerializer,
                                             WorkoutCreateSerializer, WorkoutUpdateSerializer)
from wog_workout.serializers.session import (WorkoutSessionResponseSerializer, WorkoutSessionCreateSerializer,
                                             WorkoutSessionUpdateSerializer, SessionResponseSerializer)
from wog_workout.serializers.progression import (WorkoutProgressionResponseSerializer,
                                                 WorkoutProgressionCreateSerializer)


####################################################
# WORKOUTS
####################################################
class WorkoutViewSet(ListMixin, RetrieveMixin,
                     CreateMixin, UpdateMixin, DestroyMixin,
                     WogViewSet):
    # To access the Workouts, the user must be authenticated
    # and have permissions object-level permissions
    permission_classes = (IsAuthenticated, IsWorkoutCreatorOrReadOnly)

    update_serializer_class = WorkoutUpdateSerializer
    create_serializer_class = WorkoutCreateSerializer
    response_serializer_class = WorkoutReadOnlySerializer
    serializer_class = WorkoutReadOnlySerializer
    """
    API viewset that allows projects to be viewed or edited.
    """
    queryset = Workout.objects.filter(is_active=True).select_related('creator')
    # filter_backends = (filters.DjangoObjectPermissionsFilter,)

    def get_queryset(self):
        
        wod_queryset = self.queryset.filter(Q(creator=self.request.user) | Q(is_public=True))
        
        # Checking Query Parameter in URL
        workout_type = self.request.query_params.get('type', None)
        if workout_type == 'private':
            return wod_queryset.filter(creator=self.request.user)
        elif workout_type == 'public':
            return wod_queryset.filter(is_public=True, is_staff=False)
        elif workout_type == 'staff':
            return wod_queryset.filter(is_public=True, is_staff=True)
        else:
            return wod_queryset


####################################################
class NestedInWorkoutViewSet(WogViewSet):
    """Verify that the user has access to a Workout."""
    # Perform authorization validation on the workout
    permission_classes = (IsAuthenticated, IsWorkoutCreatorOrReadOnly)

    def get_workout_id(self):
        """Return the reference to the workout."""
        return self.kwargs['workout_pk']

    def get_workout(self):
        """Return the referenced workout."""
        return get_object_or_404(Workout.objects.all(), pk=self.get_workout_id())

    def filter_on_workout(self, queryset):
        return queryset.filter(workout=self.get_workout_id())


class SessionInWorkoutViewSet(WogViewSet, ListMixin, RetrieveMixin,
                            CreateMixin, UpdateMixin, DestroyMixin):

    permission_classes = (IsAuthenticated, IsSessionCreatorOrReadOnly)

    response_serializer_class = WorkoutSessionResponseSerializer
    create_serializer_class = WorkoutSessionCreateSerializer
    update_serializer_class = WorkoutSessionUpdateSerializer

    def get_queryset(self):
        return WorkoutSession.objects.filter(workout=self.kwargs['project_pk'])
                            #.prefetch_related('project_permissions', 'related_user')


class WorkoutSessionViewSet(WogViewSet, RetrieveMixin, ListMixin):

    permission_classes = (IsAuthenticated,)
    queryset = WorkoutSession.objects.all()
    response_serializer_class = SessionResponseSerializer

    def get_queryset(self):
        return WorkoutSession.objects.filter(permission_groups__users__in=[self.request.user])


class WorkoutProgressionViewSet(WogViewSet, ListMixin, RetrieveMixin,
                                CreateMixin, DestroyMixin):
    
    permission_classes = (IsAuthenticated,)
    queryset = WorkoutProgression.objects.all()
    response_serializer_class = WorkoutProgressionResponseSerializer
    create_serializer_class = WorkoutProgressionCreateSerializer

    def get_queryset(self):
        return self.queryset.filter(session=self.kwargs['session_pk'])
