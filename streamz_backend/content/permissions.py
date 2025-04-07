from rest_framework import permissions

class HasActiveSubscription(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con suscripción activa.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'subscription_active') and
            request.user.subscription_active
        )