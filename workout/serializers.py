from rest_framework import serializers

from exercise.serializers import ExerciseSerializer
from round.models import Round, Step
from workout.models import Workout, WorkoutTree


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Used as a homepage for the workout
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Workout
        fields = ('name', 'type', 'creator')

    def get_type(self,obj):
        return obj.get_type_display()


class WorkoutListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Used to display a synthetic list of workouts
    """
    class Meta:
        model = Workout
        fields = ('name', 'url')


class StepSerializer(serializers.ModelSerializer):
    """
    Retrieve the detailed informations of a step (using Exercise detail).
    Used to build the detailed of a Round model instance.
    """
    exercise = ExerciseSerializer()
    
    class Meta:
        model = Step
        fields = ('id', 'nb_rep', 'exercise', 'weight')


class RoundSerializer(serializers.ModelSerializer):
    """
    A round is a container for steps.
    """
    round_steps = StepSerializer(many=True)
    class Meta:
        model = Round 
        fields = ('nb_repeat', 'round_steps')

class WorkoutDetailSerializer(serializers.ModelSerializer):
#     round = serializers.CharField(source='workoutitemnode.round')
#     step = serializers.CharField(source='workoutitemnode.step')
    name = serializers.CharField()

    class Meta:
        model = Workout
        fields = ('name',)

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

