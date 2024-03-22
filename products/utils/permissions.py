from django.contrib.auth.models import Permission
from rest_framework import permissions

def check_permission(user):

    if not user.is_authenticated:
        return False
    
    if user.role_id == 1:#Se for Master, pode tudo.
        return True
    
    return True


class MinimumAuthorization(permissions.BasePermission):
    message = 'O usuário não tem autorização para essa ação.'

    def has_permission(self, request, _view):
        return check_permission(request.user)

