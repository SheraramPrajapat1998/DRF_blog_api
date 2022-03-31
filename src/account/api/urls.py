from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .import views

urlpatterns = [
    path('users/', views.UserListAPIView.as_view(), name=views.UserListAPIView.name),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name=views.UserDetailAPIView.name),
    path('users/register/', views.UserRegisterAPIView.as_view(), name=views.UserRegisterAPIView.name),
    path('token/', views.MyTokenObtainPairView.as_view(), name=views.MyTokenObtainPairView.name),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]