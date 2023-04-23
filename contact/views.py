from django.shortcuts import (
                              render,
                              reverse,
                              get_object_or_404,
                              redirect
                              )
from .forms import ContactForm
from django.contrib import messages


def contact(request):
    """A view to return contact form and page"""
    form = ContactForm()

    """customer must be logged in to prevent spam."""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to contact us')
        return redirect(reverse('home:home'))

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent')
            return redirect(reverse('home:home'))
        else:
            messages.error(request,
                           'Something went wrong. Please try again later')
    else:
        form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def faq(request):
    """return faq template"""
    template = 'contact/faq.html'
    return render(request, template)


def shipping(request):
    """return faq template"""
    template = 'contact/shipping.html'
    return render(request, template)


def returns(request):
    """returns template"""
    template = 'contact/returns.html'
    return render(request, template)


def about(request):
    """about template"""
    template = 'contact/about.html'
    return render(request, template)
