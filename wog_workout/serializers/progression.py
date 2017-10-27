import pytz
import datetime as dt
from annoying.functions import get_object_or_None
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound, ValidationError

from wog_workout.models import WorkoutSession, WorkoutProgression
from wog_round.models import Step


class WorkoutProgressionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutProgression
        fields = ('__all__')


class WorkoutProgressionCreateSerializer(serializers.ModelSerializer):
    time = serializers.IntegerField(required=False)

    def validate(self, attrs):
        session = get_object_or_404(WorkoutSession, pk=self.context['view'].kwargs['session_pk'])
        user = self.context['request'].user
        
        try:
            last_progress = WorkoutProgression.objects.filter(session=session, user=user).latest('created_at')
            attrs['step'] = last_progress.step + 1
            attrs['time'] = (dt.datetime.utcnow().replace(tzinfo=pytz.utc) - last_progress.created_at).total_seconds()
        except WorkoutProgression.DoesNotExist:
            attrs['step'] = 0
            attrs['time'] = 0

        # Control if last step of the workout have been completed
        if attrs['step'] > session.workout.get_step_count():
            raise ValidationError('Max step already done')

        attrs['session'] = session
        attrs['user'] = user

        return attrs

    class Meta:
        model = WorkoutProgression
        fields = ('time',)


class WorkoutProgressionDeleteSerializer(serializers.Serializer):

    def validate(self, attrs):
        try:
            last_progress = WorkoutProgression.objects.filter(session=session, user=user).latest('created_at')
            attrs['progression'] = last_progress
        except WorkoutProgression.DoesNotExist:
            raise NotFound()

    def save(self):
        return self.validated_data['progression']