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

class WorkoutTreeSerializer(serializers.ModelSerializer):
    round = serializers.CharField(source='workoutitemnode.round')
    step = serializers.CharField(source='workoutitemnode.step')

#     def get_item(self, obj):
#         return 'item'
#         if obj.round is not None:
#             return obj.round
#         elif obj.step is not None:
#             return obj.step
    
    class Meta:
        model = WorkoutTree
        fields = ('round', 'step',)

class WorkoutTreeDetailSerializer(serializers.ModelSerializer):
    """
    Used to get detailed vision of a workout > rounds > steps > exercises
    """
    #id = serializers.IntegerField(source='gantttreeitem.task.id')
    #rounds = RoundSerializer(many=True)
    items = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    
    def get_items(self, obj):
        queryset = WorkoutTree.objects.filter(workoutitemnode__round__workout=obj, workoutitemnode__step__workout=obj)
        serializer = WorkoutTreeSerializer(queryset, many=True)
        return serializer.data
    
    def get_type(self,obj):
        return obj.get_type_display()
        
    class Meta:
        model = WorkoutTree
        fields = ('__all__')
        
        

