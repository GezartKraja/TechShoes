from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    products = cart.get_product
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request,'cart_summary.html',{'cart_product':products, 'quantities':quantities, 'totals':totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test or POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in database
        product = get_object_or_404(Product, id=product_id)
        # Save to session
        cart.add(product=product, quantity=product_qty)
        # Get cart quantity
        cart_quantity = cart.__len__()
        # Return response
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response