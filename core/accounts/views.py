from django.db.models.query import QuerySet
from typing import Any

from .forms import (
    CustomUserCreationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    LoginForm,
    CreatePostForm,
)
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
    update_session_auth_hash,
)
from django.views.generic import ListView, UpdateView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from blog.models import Post
from .mixins import (
    AccessOwnUserProfileMixin,
    LimitAccessUserProfileFieldMixin,
    AccessSuperUserOnly,
    AccessOwnPostMixin,
)
from django.urls import reverse_lazy


#################################
##### Login Page
#################################
def login_view(request):
    # If the user was logged in and we clicked on login again, don't display the login
    if request.user.is_authenticated:
        return redirect("accounts:home_panel")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["email"], password=cd["password"])
            print(user)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("accounts:home_panel")
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است")

    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "pages/accounts/login.html", context)


#################################
##### Logout Page
#################################
class CustomLogoutView(LogoutView):
    """This view for logout user"""

    template_name = "pages/accounts/logout.html"


#################################
##### User List Page
#################################
class UserListView(LoginRequiredMixin, AccessSuperUserOnly, ListView):
    model = get_user_model()
    template_name = "pages/accounts/user_list.html"
    queryset = get_user_model().objects.all()
    context_object_name = "user_list"


#################################
##### Activate User Page
#################################
class ActiveUserView(View):
    """view for activation user based on token"""

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and self.activate_user(user, token):
            messages.success(
                request, "ایمیل شما فعال شد . اکنون میتوانید وارد پنل خود شوید"
            )
            return redirect("accounts:login")
        else:
            messages.error(request, "لینک مورد نظر معتبر نیست")
            return redirect("accounts:login")

    # check user is exist
    def get_user(self, uidb64):
        User = get_user_model()
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def activate_user(self, user, token):
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return True
        else:
            return False


#################################
##### SignUp Page
#################################
class SignUpView(CreateView):
    """This view for register with confirm mail"""

    template_name = "pages/accounts/signup.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # send mail confirm
        email = form.cleaned_data["email"]
        send_active_email(self.request, user, to_email=email)
        return redirect("accounts:login")


#################################
##### Password Change Page
#################################
@login_required
def password_change_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "کلمه عبور با موفقیت عوض شد")
            return redirect("accounts:logout")

    else:
        form = CustomPasswordChangeForm(request.user)

    context = {"form": form}
    return render(request, "pages/accounts/password_change_confirm.html", context)


#################################
##### Password Reset Page
#################################
def password_reset_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_user_model().objects.filter(email=email).first()

            # check if user exist in db
            if user is not None:
                # information email sent
                subject = "درخواست باز نشانی کلمه عبور"
                message = render_to_string(
                    template_name="pages/accounts/template_reset_password_email.html",
                    context={
                        "user": user.first_name,
                        "domain": get_current_site(request).domain,
                        "user_id": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )

                email = EmailMessage(subject=subject, body=message, to=[user.email])

                if email.send():
                    messages.success(
                        request, "لینک تعویض کلمه عبور به ایمیل شما ارسال شد"
                    )
                else:
                    messages.error(request, "ایمیل ارسال نشد خطایی رخ داده")

                return redirect("accounts:password_reset")
            else:
                messages.error(request, "کاربری با این ایمیل وجود ندارد")
    else:
        form = CustomPasswordResetForm()

    context = {"form": form}

    return render(request, "pages/accounts/password_reset.html", context)


#################################
##### Password Reset Confirm Page
#################################
def password_reset_confirm_view(request, uidb64, token):
    User = get_user_model()

    # get user by id
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "کلمه عبور شما عوض شد")
                return redirect("accounts:login")
        else:
            form = CustomSetPasswordForm(user)
        return render(
            request, "pages/accounts/password_reset_confirm.html", {"form": form}
        )
    else:
        messages.error(request, "لینک اکسپایر شده")

    return redirect("pages:home_page")


#################################
##### Home Panel Page.
#################################
class PostList(LoginRequiredMixin, ListView):
    """
    This view displays the articles of each user only to self user
    but superuser can see all article
    """

    model = Post
    template_name = "pages/accounts/post_list_panel.html"
    context_object_name = "post_list"

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author__id=self.request.user.id)


#################################
##### Profile Page
#################################
class ProfileView(
    LoginRequiredMixin,
    AccessOwnUserProfileMixin,
    LimitAccessUserProfileFieldMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """This view for edit profile user"""

    model = get_user_model()
    template_name = "pages/accounts/profile.html"
    pk_url_kwarg = "user_id"
    success_message = "پروفایل شما با موفقیت بروز رسانی شد"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super().get_form(form_class)
        form.fields["last_login"].disabled = True
        return form


#################################
##### Create Post Page
#################################
class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = "pages/accounts/create_update_post.html"
    form_class = CreatePostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        messages.success(self.request, "مقاله شما با موفقیت ثبت گردید")
        return redirect("accounts:home_panel")


#################################
##### Edit Post Page
#################################
class UpdatePostView(
    LoginRequiredMixin, AccessOwnPostMixin, SuccessMessageMixin, UpdateView
):
    model = Post
    template_name = "pages/accounts/create_update_post.html"
    form_class = CreatePostForm
    pk_url_kwarg = "post_id"
    success_message = "مقاله شما با موفقیت بروزرسانی شد"
    success_url = reverse_lazy("accounts:home_panel")


#################################
##### Delete Post Page
#################################
@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.user.id:
        messages.error(request, "شما صاحب مقاله نیستید")
        return redirect("accounts:home_panel")

    if request.method == "POST":
        post.delete()
        messages.success(request, "مقاله مورد نظر با موفقیت حذف شد")
        return redirect("accounts:home_panel")

    return render(request, "pages/accounts/delete_post.html")


def send_active_email(request, user, to_email):
    # Email informations
    subject = "فعال سازی اکانت"
    message = render_to_string(
        template_name="pages/accounts/template_activate_account_email.html",
        context={
            "user": f"{user.first_name} {user.last_name}",
            "domain": get_current_site(request).domain,
            "user_id": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    email = EmailMessage(subject=subject, body=message, to=[to_email])

    if email.send():
        messages.success(request, "کاربر گرامی لینگ فعال سازی به ایمیل شما ارسال شد")
