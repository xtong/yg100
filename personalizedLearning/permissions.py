from rest_framework import permissions

class IsParentOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.name == request.data['c_name'] and
                obj.birth_date == request.data['c_birthday'] and
                obj.birth_province == request.data['c_province'])