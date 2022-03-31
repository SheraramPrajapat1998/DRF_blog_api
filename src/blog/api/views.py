from blog.models import Post

from .import serializers
from rest_framework import permissions
from rest_framework import generics
from core.api.permissions import IsStaffOrAuthorOrReadOnly

class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all().order_by('-id')
    name = 'post-list'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all().order_by('-id')
    name = 'post-detail'
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
