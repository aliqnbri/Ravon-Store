from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin
from core.managers import export_to_csv
from typing import List, Tuple ,Type ,Callable
from account.models import CustomerProfile

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    The forms to add and change user instances
    """
    form: Type[UserAdminChangeForm] = UserAdminChangeForm
    add_form: Type[UserAdminCreationForm] = UserAdminCreationForm

    list_display: List[str] = ['username', 'email', 'role']
    list_filter: List[str] = ['role',]
    fieldsets: Tuple[Tuple[str, dict], Tuple[str, dict], Tuple[str, dict]] = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'role')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
         ),
    )
    search_fields: List[str] = ['username', 'email']
    ordering: str = '-created'
    list_per_page = 10
    filter_horizontal: Tuple = ()
    actions = [export_to_csv]


admin.site.register(User, CustomUserAdmin)

