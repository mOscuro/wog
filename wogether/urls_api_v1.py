from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from user_account.views import UserAccountViewSet
from workout.views import WorkoutViewSet, WorkoutDetailView
from exercise.views import ExerciseViewSet, EquipmentViewSet
from round.views import RoundInWorkoutViewSet, StepsInWorkoutView, StepInWorkoutViewSet


router = routers.DefaultRouter()
router.register(r'users', UserAccountViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'equipments', EquipmentViewSet)

router.register(r'workouts', WorkoutViewSet)
workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'rounds', RoundInWorkoutViewSet, base_name='workout-rounds')
workouts_router.register(r'steps', StepsInWorkoutView, base_name='workout-steps')

rounds_router = routers.NestedSimpleRouter(workouts_router, r'rounds', lookup='round')
rounds_router.register(r'steps', StepInWorkoutViewSet, base_name='round-steps')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^', include(rounds_router.urls)),
    url(r'^obtain-auth-token/$', obtain_auth_token),
]