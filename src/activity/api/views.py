from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from activity.models import Activity
from .import serializers
from core.api.permissions import IsUserOrReadOnly
class ActivityListAPIView(generics.ListCreateAPIView):
    queryset = Activity.objects.select_related('user').order_by('id')
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.ActivitySerializer
    name = 'activity-list'


class ActivityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.select_related('user').order_by('id')
    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOrReadOnly)
    serializer_class = serializers.ActivityDetailSerializer
    name = 'activity-detail'
