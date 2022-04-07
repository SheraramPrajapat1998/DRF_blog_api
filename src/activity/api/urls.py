from django.urls import path

from .import views

urlpatterns = [
    path('', views.ActivityListAPIView.as_view(), name=views.ActivityListAPIView.name),
    path('<int:pk>/', views.ActivityDetailAPIView.as_view(), name=views.ActivityDetailAPIView.name),
]