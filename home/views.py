from django.shortcuts import render

# Create your views here.


def home(request):
    '''
        this view render the home page.
    '''
    template_name = 'home/home.html'
    context = {}
    return render(request, template_name, context)
