from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение и удаление — только автору
        return obj.author == request.user
