from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 update_session_auth_hash
                                 )
from django.contrib.auth.decorators import login_required
from django.utils.encoding import (force_bytes,
                                   force_text,
                                   DjangoUnicodeDecodeError
                                   )
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from . utils import token_generator
from .models import Profile, CustomUser
from .forms import (CustomUserCreationForm,
                    CustomUserChangeForm,
                    ImageForm,
                    AddressForm
                    )
import json
import re

# Create your views here.


def index(request):
    '''
        this view renders the profile page of a logged in user
    '''
    context = {}
    template_name = 'account/profile.html'
    return render(request, template_name, context)


class RegistrationView(View):
    '''
        this view shows the registration form and enables user to
        register an account
    '''
    def get(self, request):
        context = {}
        template_name = 'account/register.html'
        return render(request, template_name, context)

    def post(self, request):
        regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
        reg_form = CustomUserCreationForm()
        template_name = 'account/register.html'
        context = {'reg_form': reg_form}
        if request.method == 'POST':
            reg_form = CustomUserCreationForm(request.POST)
            field_vals = request.POST
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            context = {'reg_form': reg_form, 'field_vals': field_vals}
            if len(username) == 0 or len(password1) == 0:
                messages.error(request, 'all fields are required.')
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=400
                            )
            if len(username) < 2 or len(username) > 20:
                messages.error(
                    request,
                    'username must be between 2 or 20 characters.'
                    )
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=406
                            )
            if not username.isalnum():
                messages.error(
                            request,
                            'Only alpha numeric characters allowed.'
                            )
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=400
                            )
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=404
                            )
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Email already taken, choose another.')
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=409
                            )
            if not (re.search(regex, email)):
                messages.error(request, 'Email is invalid.')
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=400
                            )
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken, choose another.')
                return render(
                            request,
                            'account/register.html',
                            context,
                            status=409
                            )
            user = User.objects.create_user(
                                            username=username,
                                            email=email,
                                            password=password1
                                            )
            user.set_password(password1)
            user.is_active = False
            user.save()
            # send email to activate account
            email_subject = 'Account activation'
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('account:activate',
                            kwargs={'uidb64': uidb64,
                                    'token': token_generator.make_token(user)
                                    }
                           )
            activate_url = 'http://'+domain+link
            msg = 'please use the link below to activate your account'
            email_body = f'Hi, {user.username}, {msg} {activate_url}'
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [reg_form.cleaned_data.get('email')],
                fail_silently=False
                )
            messages.success(request, mark_safe("Account created successfully.\
                                                <br>\
                                                Check your mail to activate\
                                                account."
                                                )
                             )
            return render(request, template_name, context)
        return render(request, template_name, context)


def signin(request):
    '''
        this view shows the login form and enables
        a registered user to login the system
    '''
    context = {}
    template_name = 'account/login.html'
    return render(request, template_name, context)


def validate_username(request):
    '''
        This view enables ajax validation
        of the username input field for a
        better userexperience
    '''
    data = json.loads(request.body)
    err_str = 'Username should contain only alphanumeric characters.'
    err_str1 = 'Username must be between 2 and 20 characters.'
    err_str2 = 'Sorry username already in use, choose another.'
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse(
            {'username_error': err_str},
            status=400,
            content_type='application/json'
            )
    if len(data['username']) <= 1 or len(data['username']) >= 21:
        return JsonResponse(
            {'username_error': err_str1},
            status=406,
            content_type='application/json'
            )
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {'username_error': err_str2},
            status=409,
            content_type='application/json'
            )
    return JsonResponse(
        {'username_valid': True},
        status=200,
        content_type='application/json'
        )


def validate_email(request):
    '''
        This view enables ajax validation
        of the email input field for a
        better userexperience
    '''
    regex = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    data = json.loads(request.body)
    err_str = 'Sorry,email already taken, choose another one'
    err_str1 = 'Email is invalid.'
    email = data['email']
    if User.objects.filter(email=email):
        return JsonResponse({'email_error': err_str}, status=409)
    if (re.search(regex, email)):
        return JsonResponse({'email_valid': True}, status=200)
    else:
        return JsonResponse({'email_error': err_str1}, status=400)
