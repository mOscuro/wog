"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # APIs
    url(r'^auth/', include('wog_user.authentication.urls')),
    url(r'^auth/registration/', include('wog_user.registration.urls')),
    
    # All URLs related to REST API v1 are included in urls_api module
    url(r'^', include('wogether.urls_api')),
]


if settings.DEBUG:
    # The URLs listed below are intended to be present only when DEBUG is set to True
    urlpatterns += [
        # URLs for API Authentication
        url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

        # URLs for admin section
        url(r'^admin/', admin.site.urls),
    ]
