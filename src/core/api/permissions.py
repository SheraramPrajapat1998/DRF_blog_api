from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS


class ListReadOnly(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsUserOrReadOnly(BasePermission):
    """
    Object-level permission to only allow users of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.user == request.user


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user


class IsStaffOrUserOrReadOnly(IsUserOrReadOnly):
    """
    Object-level permission to only allow authors and staff members of an object to edit it.
    Assumes the model instance has an `author` and user instance has a `staff` attribute.
    """

    def has_object_permission(self, request, view, obj):
        perms = super().has_object_permission(request, view, obj)
        return bool(perms or request.user.is_staff)


class IsStaffOrAuthorOrReadOnly(IsAuthorOrReadOnly):
    """
    Object-level permission to only allow authors and staff members of an object to edit it.
    Assumes the model instance has an `author` and user instance has a `staff` attribute.
    """

    def has_object_permission(self, request, view, obj):
        perms = super().has_object_permission(request, view, obj)
        return bool(perms or request.user.is_staff)


class IsStaffOrReadOnly(BasePermission):
    """
    Allow only staff members.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
