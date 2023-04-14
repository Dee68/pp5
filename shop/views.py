from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review

# Create your views here.


def products(request, category_slug=None):
    """ A view to return products page """
    categories = None
    products = None
    query = None

    if category_slug is None:
        products = Product.objects.all().filter(in_stock=True)
        product_count = products.count()
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,
                                          in_stock=True)
        product_count = products.count()

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You did not enter any search creteria!")
                return redirect('shop:products')

            queries = (Q(name__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'search_term': query,
    }
    return render(request, 'shop/products.html', context)


def product_detail(request, category_slug, product_slug):
    """ A view to show individual product details """
    try:
        product = Product.objects.get(category__slug=category_slug,
                                      slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product,
    }

    template = 'shop/product_detail.html'

    return render(request, template, context)
