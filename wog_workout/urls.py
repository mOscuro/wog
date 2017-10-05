#===============================================================================
# from django.conf.urls import url, include
# from workout import views
# from rest_framework.routers import DefaultRouter
#===============================================================================

# Create a router and register our viewsets with it.
#router = DefaultRouter()
#router.register(r'workoutlist', views.WorkoutNameListViewSet)
#router.register(r'users', views.UserViewSet)

#router_test = DefaultRouter()
#router.register(r'workout', views.WorkoutViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
#urlpatterns = [
#    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#]