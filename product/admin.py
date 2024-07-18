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
    list_filter = ['name','parent']
    readonly_fields = ['created_at', 'updated_at']  # Added to hide fields from edit
    ordering = ['name']
    search_fields = ['name','parent']  # Added field to search by description
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
    
        'price',
        'is_available',
        'created_at',
        'updated_at',
    ]
    list_filter = ['is_available', 'brand', ]
    list_editable = ['brand', 'price', 'is_available']
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at',]
    # Added custom actions
    actions = ['mark_as_unis_available', 'restore_availability', export_to_csv]

    def mark_as_unis_available(self, request, queryset):
        for obj in queryset.filter(is_available=True):
            obj.is_available = False
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products marked as unis_available')

    def restore_availability(self, request, queryset):
        for obj in queryset.filter(is_available=False):
            obj.is_available = True
            obj.save()
        self.message_user(
            request, f'{queryset.count()} products restored to availability')

    def product_by_category(self, obj):
        return ', '.join([category.name for category in obj.category.all()])    

    mark_as_unis_available.short_description = 'Mark as unis_available'
    restore_availability.short_description = 'Restore availability'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
