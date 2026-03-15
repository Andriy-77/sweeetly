from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger("orders")


def send_order_confirmation(order):
    try:
        subject = f"Sweetly — Замовлення #{order.id} підтверджено"
        message = render_to_string(
            "orders/email/order_confirmation.txt", {"order": order}
        )
        html_message = render_to_string(
            "orders/email/order_confirmation.html", {"order": order}
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email відправлено для замовлення #{order.id}")
    except Exception as e:
        logger.error(f"Помилка відправки email: {e}")
