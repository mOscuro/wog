from rest_framework_nested import routers
from workouts.views import WorkoutViewSet, StepNestedInWorkoutViewSet
from django.conf.urls import url, include
from exercises.views import ExerciseViewSet

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'workouts', WorkoutViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'exercises', ExerciseViewSet)


workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'steps',
                          StepNestedInWorkoutViewSet,
                          base_name='workout-steps')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
]