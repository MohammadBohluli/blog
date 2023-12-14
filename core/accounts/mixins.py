from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import CustomUser


class AccessOwnUserProfileMixin:
    """This mixin forces the user to change only own profile(not other profile)"""

    def dispatch(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=user_id)
        if user.id != request.user.id:
            return PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class LimitAccessUserProfileFieldMixin:
    """This mixin limited access to special fields"""

    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "first_name",
            "last_name",
            "email",
            "last_login",
        ]
        if self.request.user.is_superuser:
            self.fields += [
                "is_active",
                "is_superuser",
                "is_staff",
            ]
        return super().dispatch(request, *args, **kwargs)
