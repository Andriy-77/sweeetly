from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<int:order_id>/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.success, name="success"),
    path("webhook/", views.webhook, name="webhook"),
]
