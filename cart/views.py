from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    products = cart.get_product
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request,'cart_summary.html',{'cart_product':products, 'quantities':quantities, 'totals':totals})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()



        # Then return the JSON response
        response = JsonResponse({'product': product_id})
        messages.success(request, ('Produkti u shtua ne shport!'))
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ('Produkti u hiq nag shporta!'))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ('Shporta u perditsua!'))
        return response
