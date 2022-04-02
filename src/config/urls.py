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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions

from account.api import views as account_api_views
from blog.api import views as blog_api_views
from category.api import views as category_api_views
from core.api import views as core_api_views
from comment.api import views as comment_api_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, format=None, **kwargs):
        return Response({
            'categories': reverse(category_api_views.CategoryListAPIView.name, request=request, format=format),
            'comments': reverse(comment_api_views.CommentListAPIView.name, request=request, format=format),
            'health_check': reverse(core_api_views.APIHealthCheck.name, request=request, format=format),
            'posts': reverse(blog_api_views.PostListCreateAPIView.name, request=request, format=format),
            'users': reverse(account_api_views.UserListAPIView.name, request=request, format=format),
            'user_register': reverse(account_api_views.UserRegisterAPIView.name, request=request, format=format),
            'swagger_endpoints': reverse('schema-swagger-ui', request=request, format=format),
       })

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="Blog API for learning DRF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=settings.EMAIL_HOST_USER),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    path('api/', include([
        path('', ApiRoot.as_view(), name=ApiRoot.name),
        path('account/', include('account.api.urls')),
        path('blog/', include('blog.api.urls')),
        path('category/', include('category.api.urls')),
        path('comments/', include('comment.api.urls')),
        path('health/', core_api_views.APIHealthCheck.as_view(), name=core_api_views.APIHealthCheck.name),
        path('swagger/', schema_view.with_ui(
            'swagger', cache_timeout=0), name='schema-swagger-ui'),
    ])),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += api_urlpatterns


# STATIC and MEDIA URLS
if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
