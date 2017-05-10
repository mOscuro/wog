from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers

from user_account.views import UserAccountViewSet
from workout.views import WorkoutViewSet, WorkoutDetailView
from exercise.views import ExerciseViewSet
from round.views import StepDetailViewSet


router = routers.DefaultRouter()
router.register(r'users', UserAccountViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'exercises', ExerciseViewSet)

router.register(r'steps', StepDetailViewSet)


workouts_router = routers.NestedSimpleRouter(router, r'workouts', lookup='workout')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(workouts_router.urls)),
    url(r'^obtain-auth-token/$', obtain_auth_token),
    # These cannot be included in NestedRouters as they do not include a specific item ID
    url(r'^workouts/(?P<workout_pk>\d+)/detail/', WorkoutDetailView.as_view(), name="workout-detail"),

]