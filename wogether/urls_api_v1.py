from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from account.views import AccountViewSet
from workout.views import WorkoutViewSet, StepNestedInWorkoutViewSet
from exercise.views import ExerciseViewSet


router = routers.DefaultRouter()
router.register(r'users', AccountViewSet)
router.register(r'workout', WorkoutViewSet)
router.register(r'exercise', ExerciseViewSet)


workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'steps',
                          StepNestedInWorkoutViewSet,
                          base_name='workout-steps')
#workouts_router.register(r'detail')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^obtain-auth-token/$', obtain_auth_token),
]