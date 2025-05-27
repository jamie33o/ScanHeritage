from django.contrib import admin
from .models import QRSignProduct, Order, OrderItem

@admin.register(QRSignProduct)
class QRSignProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'material', 'size', 'price', 'is_active']
    list_filter = ['material', 'size', 'is_active']
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['heritage_site', 'product', 'price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'shipping_name']
    readonly_fields = ['order_number', 'stripe_payment_intent_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount', 'stripe_payment_intent_id')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 
                      'shipping_city', 'shipping_state', 'shipping_zip', 'shipping_country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )