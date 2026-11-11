from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        # Автоматически назначаем автора текущим пользователем
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet дает только GET (список и детали), 
    # что соответствует заданию (создавать группы через API нельзя)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self):
        # Получаем пост по id из URL
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        # Возвращаем комментарии только для конкретного поста
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        # Сохраняем автора и привязываем к посту из URL
        serializer.save(author=self.request.user, post=self.get_post())
