from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка, что пользователь является владельцем привычки"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicHabit(permissions.BasePermission):
    """Разрешает просмотр публичных привычек"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.user == request.user
