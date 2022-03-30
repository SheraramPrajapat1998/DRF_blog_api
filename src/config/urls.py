"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from account.api import views as account_api_views
from core.api import views as core_api_views

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, format=None, **kwargs):
        return Response({
            'health_check': reverse(core_api_views.APIHealthCheck.name, request=request, format=format),
            'users': reverse(account_api_views.UserListAPIView.name, request=request, format=format),
            'user_register': reverse(account_api_views.UserRegisterAPIView.name, request=request, format=format),
       })

api_urlpatterns = [
    path('api/', include([
        path('', ApiRoot.as_view(), name=ApiRoot.name),
        path('account/', include('account.api.urls')),
        path('health/', core_api_views.APIHealthCheck.as_view(), name=core_api_views.APIHealthCheck.name),
    ])),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += api_urlpatterns
