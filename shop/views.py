from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review, Rating
from . forms import ProductForm, ReviewForm

# Create your views here.


def products(request, category_slug=None):
    """ A view to return products page """
    categories = None
    products = None
    query = None

    if category_slug is None:
        products = Product.objects.all().filter(in_stock=True)\
            .order_by('-created_at')
        product_count = products.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category,
                                          in_stock=True).order_by(
                                                                  '-created_at'
                                                                  )
        product_count = products.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.GET:
        if 'q' in request.GET:
            products = Product.objects.all().filter(in_stock=True)\
                .order_by('-created_at')
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You did not enter any search creteria!")
                return redirect(reverse('shop:products'))

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


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product).all().order_by(
                                                                '-created_at'
                                                                    )
    form = ReviewForm(request.POST)
    context = {
        'product': product,
        'reviews': reviews
    }
    template = 'shop/product_detail.html'

    return render(request, template, context)


@login_required(login_url='account:signin')
def add_review(request, product_id):
    '''
        this view enables logged in users to
        give their review
    '''
    form = ReviewForm()
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    review = Review(user=user, product=product)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review added successfully')
            return redirect(reverse('shop:product_detail', args=[product_id]))
        else:
            messages.error(request, 'All fields are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'product': product, 'user': user, 'form': form}
    return render(request, 'shop/add_review.html', context)


@login_required(login_url='account:signin')
def add_product(request):
    """ Add a product to the store by super user """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('shop:add_product'))
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
    """ Edit a product by super user"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home:home'))

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
    """Delete a product by super user"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, that action is not permitted')
        return redirect(reverse('home:home'))
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"{product.name} successfully deleted")
        return redirect(reverse('shop:products'))
    return render(request, 'shop/confirm.html', {'product': product})
