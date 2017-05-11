from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from user_account.views import UserAccountViewSet
from workout.views import WorkoutViewSet
from exercise.views import ExerciseViewSet
from round.views import RoundInWorkoutViewSet, StepsInWorkoutView


router = routers.DefaultRouter()
router.register(r'users', UserAccountViewSet)
router.register(r'exercises', ExerciseViewSet)

router.register(r'workouts', WorkoutViewSet)
workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'rounds', RoundInWorkoutViewSet, base_name='workout-rounds')
workouts_router.register(r'steps', StepsInWorkoutView, base_name='workout-steps')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^obtain-auth-token/$', obtain_auth_token),
]