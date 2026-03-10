import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderForm
from .email import send_order_confirmation

logger = logging.getLogger('orders')


def order_create(request):
    cart = Cart(request)
    if not len(cart):
        messages.warning(request, 'Кошик порожній.')
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    total=cart.get_total(),
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        name=item['product'].name,
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                request.session['order_id'] = order.id
                logger.info(f'Замовлення #{order.id} створено')
                send_order_confirmation(order)  # ← тут, всередині try
                return redirect('payments:checkout', order_id=order.id)
            except Exception as e:
                logger.error(f'Помилка створення замовлення: {e}')
                messages.error(request, 'Помилка оформлення. Спробуйте ще раз.')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.phone,
            }
        form = OrderForm(initial=initial)

    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})


@login_required
def order_history(request):
    orders = request.user.orders.prefetch_related('items__product').all()
    return render(request, 'orders/order_history.html', {'orders': orders})