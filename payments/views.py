import stripe
import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from cart.cart import Cart

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "uah",
                        "product_data": {"name": f"Замовлення #{order.id}"},
                        "unit_amount": int(order.total * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(f"/payments/success/{order.id}/"),
            cancel_url=request.build_absolute_uri("/cart/"),
            metadata={"order_id": order.id},
        )
        order.stripe_session_id = session.id
        order.save()
        return redirect(session.url, code=303)
    except Exception as e:
        logger.error(f"Stripe помилка: {e}")
        return render(request, "payments/error.html", {"message": str(e)})


def success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    Cart(request).clear()
    return render(request, "payments/success.html", {"order": order})


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        logger.error(f"Webhook помилка: {e}")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"].get("order_id")
        try:
            order = Order.objects.get(id=order_id)
            order.status = "paid"
            order.save()
            logger.info(f"Замовлення #{order_id} оплачено")
        except Order.DoesNotExist:
            logger.error(f"Замовлення #{order_id} не знайдено")

    return HttpResponse(status=200)
