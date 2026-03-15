from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product, quantity)
    return JsonResponse({"count": len(cart), "total": str(cart.get_total())})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    if quantity > 0:
        cart.add(product, quantity, override=True)
    else:
        cart.remove(product)
    return JsonResponse({"count": len(cart), "total": str(cart.get_total())})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({"count": len(cart), "total": str(cart.get_total())})
