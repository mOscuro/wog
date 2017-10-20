from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

# from exercise.serializers import ExerciseSerializer
from wog_round.serializers import RoundSerializer
from wog_user.serializers import UserAccountSerializer
from wog_workout.models import Workout, WorkoutSession


class WorkoutDetailSerializer(serializers.ModelSerializer):
    """
    Used as a homepage for the workout
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    rounds = RoundSerializer(many=True)

    def get_type(self, obj):
        return obj.get_type_display()

    class Meta:
        model = Workout
        fields = ('id', 'name', 'type', 'creator', 'rounds')


class WorkoutReadOnlySerializer(serializers.ModelSerializer):
    """
    Used to display a synthetic list of workouts
    """
    creator = UserAccountSerializer()
    
    class Meta:
        model = Workout
        fields = ('id', 'name', 'creator', 'is_public')
        read_only_fields = ('id', 'name', 'creator', 'is_public')


class WorkoutCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the class Project used when creating projects
    """
    name = serializers.CharField()

    def validate(self, attrs):
        attrs['creator'] = self.context['request'].user
        return attrs

    class Meta:
        model = Workout
        fields = ('name',)


class WorkoutUpdateSerializer(serializers.ModelSerializer):
    """
    Used to edit infos of a workout (name, visibility, time_cap....)
    """
    name = serializers.CharField(required=False)
    is_public = serializers.BooleanField(required=False)
    
    def validate(self, attrs):
        user = self.context['request'].user
        
        # Make sure there workout names are unique for each users
        workout = Workout.objects.get(id=self.context['view'].kwargs['pk'])
        if Workout.objects.filter(~Q(id=self.context['view'].kwargs['pk']), creator=workout.creator, name=attrs.get('name')):
            raise ValidationError(_('You cannot have 2 workouts with same name'))
        
        return attrs

                
    class Meta:
        model = Workout
        fields = ('id', 'name', 'is_public')


class WorkoutSessionResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutSession
        fields = ('id', 'start', 'workout', 'creator')


class WorkoutSessionCreateSerializer(serializers.ModelSerializer):

    start = serializers.DateTimeField(required=False)

    def validate(self, attrs):
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

