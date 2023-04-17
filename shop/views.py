from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from . forms import ReviewForm, ProductForm

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
        reviews = Review.objects.all()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'reviews': reviews
    }

    template = 'shop/product_detail.html'

    return render(request, template, context)


def add_review(request, prod_id):
    '''
        this view enables logged in users to
        give their review
    '''
    form = ReviewForm()
    product = get_object_or_404(Product, id=prod_id)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review added successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'All fields are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'product': product, 'user': user, 'form': form}
    return render(request, 'shop/product_detail.html', context)


@login_required(login_url='account:signin')
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home'))
    """ Add a product to the store """

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'shop/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required(login_url='account:signin')
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home:home'))

    """ Edit a product """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('shop:products'))
        else:
            messages.error(request,
                           'Failed to update product.'
                           'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'shop/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required(login_url='account:signin')
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home:home'))

    """Delete a product function"""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, f"{product.product_name} has been deleted")
    return redirect(reverse('shop:products'))
