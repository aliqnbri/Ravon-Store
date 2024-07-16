from django.contrib import admin

# Register your models here.
from core.managers import export_to_csv
from .models import Order, OrderItem



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