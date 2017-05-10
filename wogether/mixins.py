
from rest_framework import mixins, status
from rest_framework.response import Response


class ListInWorkoutMixin(mixins.ListModelMixin):
    """List objects that belongs to a Workout."""
    def list(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super().list(request, *args, **kwargs)


class RetrieveInWorkoutMixin(mixins.RetrieveModelMixin):
    """Retrieve an object that belongs to a Workout."""
    def retrieve(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super().retrieve(request, *args, **kwargs)


class UpdateInWorkoutMixin(mixins.UpdateModelMixin):
    """Update an object that belongs to a Workout."""
    def update(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Verify update is valid and perform it
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the object serialized
        instance = self.get_object()
        serializer = self.get_response_serializer(instance)
        return Response(serializer.data)


class DestroyInWorkoutMixin(mixins.DestroyModelMixin):
    """Destroy an object that belongs to a Workout."""
    def destroy(self, request, *args, **kwargs):
        self.get_workout(workout_pk=kwargs['workout_pk'])
        return super().destroy(request, *args, **kwargs)


class CreateInWorkoutMixin(mixins.CreateModelMixin):
    """Create an object that belongs to a Workout."""
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
