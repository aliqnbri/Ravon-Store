from django.contrib import admin
from account.models import CustomUser 
from account.forms import CustomUserCreationForm , CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from core.managers import export_to_csv
from django.utils.translation import gettext_lazy as _
from customer.models import Address

admin.site.site_header = 'Ali Qanbari Admin'
admin.site.site_title = 'Ali Qanbari'
admin.site.index_title = 'Ali Qanbari administration'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form= CustomUserCreationForm
    model = CustomUser
    list_display = ('email', 'role', 'is_active',)
    list_filter = ('is_active','role' ,'staff_role')
    fieldsets = (
        (_('Account Info'), {'fields': ('id', 'username', 'email', 'phone_number')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Privileges'), {
            'fields': ('role', 'staff_role', 'is_active', 'is_verified'),
        }),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'staff_role', 'is_active',)}
         ),
    )
    readonly_fields = ['is_verified', 'id']
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ()

class AddressInline(admin.StackedInline):
    model = Address
    can_delete = True
    verbose_plural_name = "Addresses"
    fk_name = 'customer'
    extra = 1