from django.contrib import admin

# Register your models here.
from core.managers import export_to_csv
from .models import Order, OrderItem ,Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'product', 'discount', 'discount_amount', 'expiration_date', 'valid_from', 'is_active']
    list_filter = ['is_active', 'valid_from', 'expiration_date', 'product']
    search_fields = ['code', 'product']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer',
                    'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at',]
    inlines = [OrderItemInline]
    actions = [export_to_csv]