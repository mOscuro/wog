from django.db import models
from treebeard.exceptions import InvalidPosition
from treebeard.mp_tree import MP_Node


class WorkoutTree(MP_Node):
    node_order_by = None
    
    
class WorkoutTreeItem(WorkoutTree):
    
    workout = models.ForeignKey('workout.Workout', related_name='workout_tree_item', on_delete=models.CASCADE)
    
    def has_tree_problems(self):
        problems = self.find_problems()
        print(problems)
        return (sum([len(problems[i]) for i in range(len(problems))]) != 0)
    
class RoundTreeItem(WorkoutTree):
    
    round = models.ForeignKey('round.Round', related_name='round_tree_item', on_delete=models.CASCADE)


class StepTreeItem(WorkoutTree):
    
    step = models.ForeignKey('round.Step', related_name='step_tree_item', on_delete=models.CASCADE)
    
    def move_up(self):
        try:
            self.move(self.get_prev_sibling(), 'left')
        except:
            raise InvalidPosition()

    def move_down(self):
        try:
            self.move(self.get_next_sibling(), 'right')
        except:
            raise InvalidPosition()

#     def move(self, target, pos=None):
#         # First check status of target
#         if isinstance(target, TaskStatus) and self.task.status != target:
#             if pos not in ['first-child', 'last-child']:
#                 raise InvalidPosition()
#             self.task.status = target
#             self.task.save()
#         elif isinstance(target, TodoTreeItem) and self.task.status != target.task.status:
#             if pos not in ['right', 'left']:
#                 raise InvalidPosition()
#             self.task.status = target.task.status
#             self.task.save()
#         # Then move item
#         return super(TodoTreeItem, self).move(target, pos=pos)