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

class ProductPermission(permissions.BasePermission):
    message = 'Você não pode alterar um produto.'

    def has_permission(self, request, _view):
        return request.user.role_id < 3
    
class ConfigPermission(permissions.BasePermission):
    message = 'Você não pode acessar configurações.'

    def has_permission(self, request, _view):
        return request.user.role_id < 3

