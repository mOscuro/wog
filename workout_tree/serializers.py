from rest_framework import serializers

from exercise.serializers import ExerciseSerializer
from workout_tree.models import StepTreeItem, RoundTreeItem, WorkoutTreeItem


class WorkoutTreeStepSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Step instance data in Tree viewset
    """
    id = serializers.IntegerField(source='steptreeitem.step.id')
    exercise = ExerciseSerializer(source='steptreeitem.step.exercise')
    item_type = serializers.SerializerMethodField()
    
    def get_item_type(self, obj):
        return "Step"
    
    class Meta:
        model = StepTreeItem
        fields = ('id', 'item_type', 'nb_rep', 'exercise', 'weight', 'distance')


class WorkoutTreeRoundSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Round instance data in Tree viewset
    """
    id = serializers.IntegerField(source='roundtreeitem.round.id')
    round_steps = WorkoutTreeStepSerializer(many=True)
    item_type = serializers.SerializerMethodField()
    
    def get_item_type(self, obj):
        return "Round"
        
    class Meta:
        model = RoundTreeItem
        fields = ('id', 'item_type', 'nb_repeat', 'round_steps')
        

class WorkoutTreeSerializer(serializers.ModelSerializer):
    """
    Serializer used to display Workout instance data in Tree viewset.
    It shows details for related items (Steps and Rounds) using dedicated serializers
    """
    id = serializers.IntegerField(source='workouttreeitem.workout.id')
    name = serializers.CharField(source='workouttreeitem.workout.name')
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
        model = WorkoutTreeItem
        fields = ('id', 'name', 'items')
