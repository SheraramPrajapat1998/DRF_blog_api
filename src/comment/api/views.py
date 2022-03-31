from rest_framework import generics

from .import serializers
from rest_framework import permissions
from comment.models import Comment
from core.api.permissions import IsStaffOrUserOrReadOnly

class CommentListAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = serializers.CommentSerializer
    name = 'comment-list'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsStaffOrUserOrReadOnly, )
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    name = 'comment-detail'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
