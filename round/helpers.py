from django.utils.translation import ugettext_lazy as _

from round.models import Round, Step

def create_round(params):
    """
    Helper function that creates a round based on keyword arguments.
    """
    if params.get('workout', None) is not None:
        workout = params.get('workout')
    else:
        raise AttributeError(_('missing parameters [workout]'))

    return Round.objects.create(_workout=workout,
                               nb_repeat=params.get('nb_repeat', 1))

def create_step(params):
    """
    Helper function that creates a step based on keyword arguments.
    Order of priority:

    * round
    * workout
    """
    if params.get('round', None) is not None:
        workout = params.get('round').get_workout()
    elif params.get('workout', None) is not None:
        workout = params.get('workout')
    else:
        raise AttributeError(_('missing parameters [workout or round]'))

    return Step.objects.create(_workout=workout,
                               _round=params.get('round', None),
                               exercise=params.get('exercise', None),
                               nb_rep=params.get('nb_rep', 1),
                               distance=params.get('distance', 1))


def insert_task_in_todo(*args, **kwargs):
    pass #return Task.objects.todo_insert(*args, **kwargs)


def insert_task_in_gantt(*args, **kwargs):
    pass #return Task.objects.gantt_insert(*args, **kwargs)
