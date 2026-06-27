from rest_framework.permissions import BasePermission

class StaffNoEditDelete(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.user.role == "OWNER":
            return True
        if request.method in ["PUT","PATCH","DELETE"]:
            return False
        return True