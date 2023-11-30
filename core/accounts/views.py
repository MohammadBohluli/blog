from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token


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
        messages.success(request,"لینک مورد نظر معتبر نیست")
    return redirect('pages:home_page')


#################################
##### Login Page
#################################
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:profile')
            else:
                return HttpResponse("Invalid login or Your account is not active")
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
    return redirect('accounts:login')


#################################
##### Register Page(with email confirmations)
#################################
def register_view(request):

    if request.method == "POST":
    
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()


            email = form.cleaned_data.get('email')
            active_email(request, user, to_email=email)
            return redirect('pages:home_page')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/register_page.html', context)


#################################
##### Profile Page
#################################
@login_required
def profile_view(request):
    return render(request, 'pages/accounts/profile.html')

#################################
##### Password Change Page
#################################
def password_change_view(request):
    pass


def active_email(request, user, to_email):
    # Email informations
    subject = "اکانت شما با موفقیت فعال شد"
    message = render_to_string(
        template_name='pages/accounts/activate_account_email.html',
        context= {
            'user': user.first_name,
            'domain': get_current_site(request).domain,
            'user_id':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )
    email = EmailMessage(subject=subject, body=message, to=[to_email])

    if email.send():
        messages.success(request,"کاربر گرامی لطفا ایمیل خود را فعال کنید")
    else:
        messages.error(request,"ایمیل ارسال نشد خطایی رخ داده")
