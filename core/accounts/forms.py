from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from blog.models import Post
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email","first_name","last_name",)


class LoginForm(forms.Form):
    email = forms.EmailField(label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='کلمه عبور')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fileds = ["old_password", "new_password1", "new_password2"]


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = get_user_model()
        fields = ['email']


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password1']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']