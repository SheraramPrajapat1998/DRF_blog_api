from django.urls import path

from category.api import views


urlpatterns = [
    path('', views.CategoryListAPIView.as_view(), name=views.CategoryListAPIView.name),
    path('<int:pk>/', views.CategoryDetailAPIView.as_view(), name=views.CategoryDetailAPIView.name),
]