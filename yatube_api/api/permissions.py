"""Разрешения для взаимодействия пользователей с эндпойнтами."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrSafeReader(BasePermission):
    """Просмотр списков объектов доступен всем пользователям,
    добавление объектов, просмотр деталей объектов доступен
    только авторизованным пользователям,
    редактирование и удаление объектов доступно только авторам объектов.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )
