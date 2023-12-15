from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import CustomUser
from blog.models import Post


class AccessOwnUserProfileMixin:
    """
    This mixin forces the user to edit only own profile(not other profile)
    but superuser can edit all profile
    """

    def dispatch(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=user_id)

        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if user.id != request.user.id:
            raise PermissionDenied
        else:
            return super().dispatch(request, *args, **kwargs)


class AccessOwnPostMixin:
    """This mixin limited access users to own post"""

    def dispatch(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if post.author.id != self.request.user.id:
            messages.error(request, "شما صاحب مقاله نیستید")
            return redirect("accounts:home_panel")

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


class AccessSuperUserOnly:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
