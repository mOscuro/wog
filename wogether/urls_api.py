from django.conf.urls import url, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from wog_user.views import UserAccountViewSet
from wog_workout.views import (WorkoutViewSet,
                               SessionInWorkoutViewSet, WorkoutSessionViewSet,
                               WorkoutProgressionViewSet, WorkoutSessionLeaderboardView)
from wog_exercise.views import ExerciseViewSet, EquipmentViewSet
from wog_round.views import RoundInWorkoutViewSet, StepInWorkoutViewSet
from rest_framework_swagger.views import get_swagger_view
    

router = routers.DefaultRouter()
router.register(r'users', UserAccountViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'equipments', EquipmentViewSet)

router.register(r'workouts', WorkoutViewSet)
workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'rounds', RoundInWorkoutViewSet, base_name='workout-rounds')
workouts_router.register(r'steps', StepInWorkoutViewSet, base_name='workout-steps')
workouts_router.register(r'sessions', SessionInWorkoutViewSet, base_name='workout-sessions')

router.register(r'sessions', WorkoutSessionViewSet)
sessions_router = routers.NestedSimpleRouter(router, r'sessions', lookup='session')
sessions_router.register(r'progressions', WorkoutProgressionViewSet, base_name='session-progressions')
sessions_router.register(r'leaderboard', WorkoutSessionLeaderboardView, base_name='session-leaderboard')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^', include(sessions_router.urls)),
    # url(r'^obtain-auth-token/$', obtain_auth_token),
    url(r'^docs/$', get_swagger_view(title='Wogether API')),
]