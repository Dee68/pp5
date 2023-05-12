from django.shortcuts import render

# Create your views here.


def home(request):
    '''
        this view render the home page.
    '''
    template_name = 'home/home.html'
    return render(request, template_name)


def terms(request):
    '''
        this view renders the terms of use
    '''
    template_name = 'home/terms.html'
    return render(request, template_name)


def privacy(request):
    '''
        this view renders the privacy policies of
        lamad shop
    '''
    template_name = 'home/privacy.html'
    return render(request, template_name)
