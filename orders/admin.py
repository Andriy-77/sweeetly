from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'status', 'total', 'created_at')
    list_filter = ('status',)
    search_fields = ('email', 'first_name', 'last_name')
    list_editable = ('status',)
    inlines = [OrderItemInline]
