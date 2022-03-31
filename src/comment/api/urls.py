from django.urls import path

from .import views

urlpatterns = [
    path('', views.CommentListAPIView.as_view(), name=views.CommentListAPIView.name),
    path('<int:pk>/', views.CommentDetailAPIView.as_view(), name=views.CommentDetailAPIView.name),
]