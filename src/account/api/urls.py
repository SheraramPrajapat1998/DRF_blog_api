from django.urls import path

from .import views

urlpatterns = [
    path('users/', views.UserListAPIView.as_view(), name=views.UserListAPIView.name),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name=views.UserDetailAPIView.name),
]
