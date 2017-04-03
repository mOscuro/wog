from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# from exercise.serializers import ExerciseSerializer
# from round.models import Round, Step
from workout.models import Workout


class WorkoutDetailSerializer(serializers.ModelSerializer):
    """
    Used as a homepage for the workout
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator')

    def get_type(self,obj):
        return obj.get_type_display()


class WorkoutListSerializer(serializers.ModelSerializer):
    """
    Used to display a synthetic list of workouts
    """
    class Meta:
        model = Workout
        fields = ('id', 'name')

class WorkoutCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the class Project used when creating projects
    """
    name = serializers.CharField()
    type = serializers.CharField(required=False)
    type = serializers.SerializerMethodField(required=False)
    creator = serializers.ReadOnlyField(source='creator.username', required=False)
    
    def get_type(self,obj):
        return obj.get_type_display()

    def validate(self, attrs):
        attrs['creator'] = self.context['request'].user
        return serializers.ModelSerializer.validate(self, attrs)

    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator')


class WorkoutDetailUpdateSerializer(serializers.ModelSerializer):
    """
    Used to edit infos of a workout (name, visibility, time_cap....)
    """
    
    def validate(self, attrs):
        workout = Workout.objects.get(id=self.context['view'].kwargs['pk'])
        if Workout.objects.filter(~Q(id=self.context['view'].kwargs['pk']), creator=workout.creator, name=attrs.get('name')):
            raise ValidationError(_('You cannot have 2 workouts with same name'))
        return serializers.ModelSerializer.validate(self, attrs)
    
    class Meta:
        model = Workout
        fields = ('id', 'name')    

