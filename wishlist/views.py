from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product
from .models import Wishlist
# Create your views here.


# @login_required(login_url='account:signin')
def whish_list(request):
    '''
        this view displays the products the user
        wishes to buy
    '''
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to signin to view this page.')
        return redirect('home:home')
    wish_list = Wishlist.objects.filter(user=request.user)
    context = {'wish_list': wish_list}
    template_name = 'wishlist/wishlist.html'
    return render(request, template_name, context)


@login_required(login_url='account:signin')
def add_to_wish_list(request):
    '''
        Adds a product to the user's
        wish list
    '''
    if request.method == 'POST':
        product_id = request.POST.get('product-id')
        product = Product.objects.get(id=product_id)
        try:
            wish_item = Wishlist.objects.get(
                                             user=request.user,
                                             product=product
                                             )
            if wish_item:
                messages.info(
                              request,
                              f'{wish_item.product.name }\
                              already in wish list.')
        except:
            Wishlist.objects.create(user=request.user, product=product)
            messages.success(request, f'Item added to wish list')
        finally:
            return HttpResponseRedirect(reverse('wishlist:wish_list'))


@login_required(login_url='account:signin')
def delete_item(request):
    '''
        Removes product item from user's wishlist
    '''
    if request.method == 'POST':
        item_id = request.POST.get('item-id')
        Wishlist.objects.filter(id=item_id).delete()
        messages.info(request, f'You have deleted the item from your wishlist')
        return HttpResponseRedirect(reverse('wishlist:wish_list'))
