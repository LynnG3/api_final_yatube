"""Представления моделей приложения yatube_api в api."""
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly)

from api.permissions import IsAuthorOrSafeReader
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Follow, Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели группы постов."""

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет модели поста. """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrSafeReader, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели комментария."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrSafeReader, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_post(self):
        """Принимает экземпляр класса коммента,
        возвращает пост, к котрому относится коммент"""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)

    def get_queryset(self):
        return self.get_post().comments.all()


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет модели подписки."""

    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
