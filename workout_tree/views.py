from rest_framework import mixins, viewsets

from workout_tree.models import WorkoutTreeItem
from workout_tree.serializers import WorkoutTreeSerializer


class WorkoutTreeViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = WorkoutTreeSerializer

    def get_queryset(self):
        return WorkoutTreeItem.objects.filter(workout=self.kwargs['workout_pk'])