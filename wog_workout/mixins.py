from rest_framework import mixins, status
from rest_framework.response import Response


class ListNestedInWorkoutMixin(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super(ListNestedInWorkoutMixin, self).list(request, *args, **kwargs)


class RetrieveNestedInWorkoutMixin(mixins.RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super(RetrieveNestedInWorkoutMixin, self).retrieve(request, *args, **kwargs)


class UpdateNestedInWorkoutMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        serializer = self.get_response_serializer(instance)

        return Response(serializer.data)


class DestroyNestedInWorkoutMixin(mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super(DestroyNestedInWorkoutMixin, self).destroy(request, *args, **kwargs)


class CreateNestedInWorkoutMixin(mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = self.perform_create(serializer)
        serializer = self.get_response_serializer(instance=saved)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
