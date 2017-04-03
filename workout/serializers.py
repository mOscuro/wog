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
    name = serializers.CharField(required=False)
    visibility = serializers.ChoiceField(choices=['staff', 'public', 'private'], required=False)
    
    def validate(self, attrs):
        user = self.context['request'].user
        
        # Make sure there workout names are unique for each users
        workout = Workout.objects.get(id=self.context['view'].kwargs['pk'])
        if Workout.objects.filter(~Q(id=self.context['view'].kwargs['pk']), creator=workout.creator, name=attrs.get('name')):
            raise ValidationError(_('You cannot have 2 workouts with same name'))
        
        type = attrs.get('type', None)
        if type is not None:
            if type == 'staff' and not user.is_staff:
                raise ValidationError(_('Standard user cannot create staff workouts'))

        return attrs
    
    def save(self):
#         type = self.validated_data.get('type', None)
#         if type is not None:
#             if type == 
        pass
                
    class Meta:
        model = Workout
        fields = ('id', 'name', 'type')    

