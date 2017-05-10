from rest_framework import status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from round.models import Step
from round.serializers import CreateStepSerializer, StepSerializer


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