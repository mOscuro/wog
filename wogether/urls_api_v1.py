from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from wog_user.views import UserAccountViewSet
from wog_workout.views import WorkoutViewSet
from wog_exercise.views import ExerciseViewSet, EquipmentViewSet
from wog_round.views import RoundInWorkoutViewSet, StepsInWorkoutView, StepInRoundViewSet


router = routers.DefaultRouter()
router.register(r'users', UserAccountViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'equipments', EquipmentViewSet)

router.register(r'workouts', WorkoutViewSet)
workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'rounds', RoundInWorkoutViewSet, base_name='workout-rounds')
#workouts_router.register(r'steps', StepsInWorkoutView.as_view(), base_name='workout-steps')

rounds_router = routers.NestedSimpleRouter(workouts_router, r'rounds', lookup='round')
rounds_router.register(r'steps', StepInRoundViewSet, base_name='round-steps')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^', include(rounds_router.urls)),
    url(r'^workouts/(?P<workout_pk>\d+)/steps/$', StepsInWorkoutView.as_view(), name='workout-steps'),
    url(r'^obtain-auth-token/$', obtain_auth_token),
]