from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from wog_workout.models import Workout, WorkoutSession


class SessionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutSession
        fields = ('__all__')

class WorkoutSessionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutSession
        fields = ('id', 'start', 'workout', 'creator')


class WorkoutSessionCreateSerializer(serializers.ModelSerializer):

    start = serializers.DateTimeField(required=False)

    def validate(self, attrs):
        print('nul')
        attrs['workout'] = get_object_or_404(Workout, pk=self.context['view'].kwargs['workout_pk'])
        attrs['creator'] = self.context['request'].user
        return attrs

    class Meta:
        model = WorkoutSession
        fields = ('start',)


class WorkoutSessionUpdateSerializer(serializers.ModelSerializer):

    start = serializers.DateTimeField()

    class Meta:
        model = WorkoutSession
        fields = ('start',)

