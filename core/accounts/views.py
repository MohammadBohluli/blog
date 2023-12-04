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
    logout,
    get_user_model,
    update_session_auth_hash
)
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from blog.models import Post


#################################
##### Login Page
#################################
def login_view(request):
    
    # If the user was logged in and we clicked on login again, don't display the login
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            print(user)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:profile')
            else:
                messages.error(request,"نام کاربری یا رمز عبور اشتباه است")

    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'pages/accounts/login.html', context)


#################################
##### Logout Page
#################################
def logout_view(request):
    logout(request)
    messages.success(request,"شما با موفقیت از اکانت خود خارج شدید")
    return redirect('accounts:login')


#################################
##### Activate User Page
#################################
def activate_user_view(request, uidb64, token):

    User = get_user_model()
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request,"ایمیل شما فعال شد . اکنون میتوانید وارد پنل خود شوید")
        return redirect('accounts:login')
    else:
        messages.error(request,"لینک مورد نظر معتبر نیست")
    return redirect('accounts:login')


#################################
##### SignUp Page(with email confirmations)
#################################
def signup_view(request):

    if request.method == "POST":
    
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()


            email = form.cleaned_data.get('email')
            send_active_email(request, user, to_email=email)
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'pages/accounts/signup.html', context)


#################################
##### Password Change Page
#################################
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'کلمه عبور با موفقیت عوض شد')
            return redirect('accounts:logout')
        
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'pages/accounts/password_change_confirm.html', context)


#################################
##### Password Reset Page
#################################
def password_reset_view(request):
    
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_user_model().objects.filter(email=email).first()

            # check if user exist in db
            if user is not None:
                # information email sent
                subject = 'درخواست باز نشانی کلمه عبور'
                message = render_to_string(
                template_name='pages/accounts/template_reset_password_email.html',
                context= {
                    'user': user.first_name,
                    'domain': get_current_site(request).domain,
                    'user_id':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }) 

                email = EmailMessage(subject=subject, body=message, to=[user.email])

                if email.send():
                    messages.success(request,"لینک تعویض کلمه عبور به ایمیل شما ارسال شد")
                else:
                    messages.error(request,"ایمیل ارسال نشد خطایی رخ داده")

                return redirect('accounts:password_reset')
            else:
                messages.error(request,"کاربری با این ایمیل وجود ندارد")
    else:
        form = CustomPasswordResetForm()
        
    context = {
        'form': form
    }

    return render(request, 'pages/accounts/password_reset.html', context)

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
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"کلمه عبور شما عوض شد")
                return redirect('accounts:login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'pages/accounts/password_reset_confirm.html', {'form': form})   
    else:
        messages.error(request,"لینک اکسپایر شده")

        
    return redirect('pages:home_page')


#################################
##### Profile Page
#################################
@login_required
def profile_view(request):
    return render(request, 'pages/accounts/profile.html')


#################################
##### Create Post Page
#################################
@login_required
def create_post_view(request):
    if request.method == "POST":
        
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("blog:post_list")
            
    else:
        form = CreatePostForm()
    
    context = {
        'form': form
    }

    return render(request, 'pages/accounts/create_update_post.html', context)

#################################
##### Edit Post Page
#################################
@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
    else:
        form = CreatePostForm(instance=post)
    context = {
        'form': form
    }

    return render(request, 'pages/accounts/create_update_post.html', context)


def send_active_email(request, user, to_email):
    # Email informations
    subject = "اکانت شما با موفقیت فعال شد"
    message = render_to_string(
        template_name='pages/accounts/template_activate_account_email.html',
        context= {
            'user': user.first_name,
            'domain': get_current_site(request).domain,
            'user_id':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )
    email = EmailMessage(subject=subject, body=message, to=[to_email])

    if email.send():
        messages.success(request,"کاربر گرامی لینگ فعال سازی به ایمیل شما ارسال شد")
