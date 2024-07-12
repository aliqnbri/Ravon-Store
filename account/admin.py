from django.contrib import admin
from django.contrib.auth import get_user_model
from account.forms import RegisterUserForm, EditUserForm
from django.contrib.auth.admin import UserAdmin
from core.managers import export_to_csv
from typing import List, Tuple ,Type 


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    The forms to add and change user instances
    """
    form: Type[EditUserForm] = EditUserForm
    add_form: Type[RegisterUserForm] = RegisterUserForm

    list_display: List[str] = ['email', 'role']
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
    search_fields: List[str] = ['email']
    # ordering = [created_at] #// have to fix this -> can not find created_at that is from BaseModel.
    list_per_page = 10
    filter_horizontal: Tuple = ()
    actions = [export_to_csv]


admin.site.register(User, CustomUserAdmin)

