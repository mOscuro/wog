from rest_framework import routers
from workouts.views import WorkoutViewSet
from django.conf.urls import url, include
from exercises.views import ExerciseViewSet

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'exercises', ExerciseViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]