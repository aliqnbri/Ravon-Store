from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Address, CustomerProfile, Comment

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'postal_code', 'secondary_address')
    list_filter = ('city', 'state', 'country')
    search_fields = ('city', 'street', 'postal_code', 'secondary_address')
    ordering = ('city', 'street')

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'gender', 'avatar')
    list_filter = ('gender',)
    search_fields = ('customer__username', 'customer__email')
    ordering = ('customer__username',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'is_published', 'customer')
    list_filter = ('is_published',)
    search_fields = ('body',)
    ordering = ('-created_at',)

admin.site.register(Address, AddressAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(Comment, CommentAdmin)