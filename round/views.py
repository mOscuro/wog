from rest_framework import status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from round.models import Step
from round.serializers import RoundSerializer, CreateStepSerializer, StepSerializer
from workout import mixins as workout_mixins
from workout.permissions import RoundObjectPermissions
from workout.views import GenericWorkoutPermissionViewSet


####################################################
# ROUNDS
####################################################
class RoundInWorkoutViewSet(workout_mixins.ListNestedInWorkoutMixin,
                               workout_mixins.RetrieveNestedInWorkoutMixin,
                               workout_mixins.UpdateNestedInWorkoutMixinn,
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
            return TaskListCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskListUpdateSerializer
        return TaskListReadOnlySerializer

    def get_queryset(self):
        return TaskList.objects.filter(project=self.kwargs['project_pk']).order_by('position')

    def perform_update(self, serializer):
        tasklist = self.get_object()
        self.check_specific_permissions(tasklist.project)
        super().perform_update(serializer)

    def perform_create(self, serializer):
        return serializer.save()

    def perform_destroy(self, instance):
        if instance.default:
            raise PermissionDenied(_('Default tasklist cannot be deleted'))
        super().perform_destroy(instance)
class StepDetailViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer
    #object_permission_class = TaskInProjectObjectPermissions
    response_serializer_class = StepSerializer


class CreateStepView(CreateAPIView):
    """
    API view used to create a step

    * `exercise`: Exercise to execute for the step (mandatory)
    * `workout`: workout for the step (optional) chosen if step is not nested in a round
    * `round`: specific round for a step (optional).

    One of the `workout` or `round` field should be present (not both)
    """
    serializer_class = CreateStepSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        step = serializer.save()
        response_serializer = StepSerializer(instance=step)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)