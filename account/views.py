from django.shortcuts import render

# Create your views here.


def index(request):
    '''
        this view renders the profile page of a logged in user
    '''
    template_name = 'account/profile.html'
    return render(request, template_name)


def register(request):
    '''
        this view shows the registration form and enables user to 
        register an account
    '''
    template_name = 'account/register.html'
    return render(request, template_name)


def signin(request):
    '''
        this view shows the login form and enables
        a registered user to login the system
    '''
    template_name = 'account/login.html'
    return render(request, template_name)
