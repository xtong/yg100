from rest_framework import permissions

class IsParentOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.name == request.data['c_name'] and
                obj.birth_date == request.data['c_birthday'] and
                obj.birth_province == request.data['c_province'])

class UserPermission(permissions.BasePermission):
    '''
    List: only staff
    Create: anyone
    Retrieve: own self or staff
    Update, Partial update: own self or staff
    Destroy: staff only
    '''
    def has_permission(self, request, view):

        if view.action == 'list':
            return request.user.is_authenticated() and request.user.is_staff
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if view.action == 'retrieve':
            return request.user.is_authenticated() and (str(obj) == str(request.user) or request.user.is_staff)
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and (str(obj) == str(request.user) or request.user.is_staff)
        elif view.action == 'destroy':
            return request.user.is_authenticated() and request.user.is_staff
        else:
            return False