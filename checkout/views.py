from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . forms import OrderForm
from .models import Order, OrderLineItem
from shop.models import Product
from cart.contexts import cart_contents
from cart.models import CartItem

# Create your views here.


def checkout(request):
    """Checkout function to to process order"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'There is nothing in your cart.')
        return redirect(reverse('shop:products'))
    order_form = OrderForm()
    template_name = 'checkout/checkout.html'
    context = {'order_form': order_form, 'cart': cart}
    return render(request, template_name, context)
