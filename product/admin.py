from django.contrib import admin

from .models import Category, Product, Brand
from core.managers import export_to_csv

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'parent',
        'products_count',  # Added field to display product count
    ]
    list_filter = ['name']
    readonly_fields = ['created', 'updated']  # Added to hide fields from edit
    ordering = ['name']
    search_fields = ['name',]  # Added field to search by description
    fields = ['name', 'slug',]  # Reordered fields
    prepopulated_fields = {'slug': ('name',)}
    actions = [export_to_csv]

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Number of products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'brand',
        'category',
        'price',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['available', 'brand', 'category',]
    list_editable = ['brand', 'category', 'price', 'available']
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created', 'updated',]
    # Added custom actions
    actions = ['mark_as_unavailable', 'restore_availability', export_to_csv]

    def mark_as_unavailable(self, request, queryset):
        for obj in queryset.filter(available=True):
            obj.available = False
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products marked as unavailable')

    def restore_availability(self, request, queryset):
        for obj in queryset.filter(available=False):
            obj.available = True
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products restored to availability')

    mark_as_unavailable.short_description = 'Mark as unavailable'
    restore_availability.short_description = 'Restore availability'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
