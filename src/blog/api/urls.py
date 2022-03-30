from django.urls import path

from .import views


urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name=views.PostListCreateAPIView.name),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name=views.PostRetrieveUpdateDestroyAPIView.name),
]