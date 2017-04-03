from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from exercise.serializers import ExerciseSerializer
from round.models import Round, Step
from workout.models import Workout, WorkoutTree


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


#---------------------------------------------------
# DEALING WITH TREES
#---------------------------------------------------

class WorkoutTreeStepSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Step instance data in Tree viewset
    """
    id = serializers.IntegerField(source='step.id')
    exercise = ExerciseSerializer()
    type = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return "Step"
    
    class Meta:
        model = Step
        fields = ('id', 'type', 'nb_rep', 'exercise', 'weight', 'distance')


class WorkoutTreeRoundSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Round instance data in Tree viewset
    """
    id = serializers.IntegerField(source='round.id')
    round_steps = WorkoutTreeStepSerializer(many=True)
    type = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return "Round"
        
    class Meta:
        model = Round 
        fields = ('id', 'type', 'nb_repeat', 'round_steps')
        

class WorkoutTreeSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Workout instance data in Tree viewset.
    It shows details for related items (Steps and Rounds) using dedicated serializers
    """
    id = serializers.IntegerField(source='workout.id')
    name = serializers.CharField(source='workout.name')
    items = serializers.SerializerMethodField()
    
    def get_items(self, obj):
        item_queryset = obj.get_children()
        
        item_serializer = []
        for item in item_queryset:
            if hasattr(item, 'round'):
                item_serializer.append(WorkoutTreeRoundSerializer(instance=item.round).data)
            elif hasattr(item, 'step'):
                item_serializer.append(WorkoutTreeStepSerializer(instance=item.step).data)
        
        return item_serializer
    
    class Meta:
        model = WorkoutTree
        fields = ('id', 'name', 'items')

