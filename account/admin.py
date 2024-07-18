from django.contrib import admin
from account.models import CustomUser , CustomerProfile , Address
from account.forms import RegisterUserForm, EditUserForm
from django.contrib.auth.admin import UserAdmin
from core.managers import export_to_csv
from typing import List, Tuple, Type

admin.site.site_header = 'Ali Qanbari Admin'
admin.site.site_title = 'Ali Qanbari'
admin.site.index_title = 'Ali Qanbari administration'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    form: Type[EditUserForm] = EditUserForm
    add_form: Type[RegisterUserForm] = RegisterUserForm






#     model = User
#     list_display = ['email','is_staff',
#                     'is_active', 'is_superuser']
#     list_filter = ['is_staff', 'is_active','is_superuser']
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('email')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active',
#          'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2',
#                        'first_name', 'last_name', 'is_staff', 'is_active')}
#          ),
#     )
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#     filter_horizontal = ()

#     list_display: List[str] = ['email', 'role']
#     list_filter: List[str] = ['role',]
#     fieldsets: Tuple[Tuple[str, dict], Tuple[str, dict], Tuple[str, dict]] = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ()}),
#         ('Permissions', {'fields': ('role',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password', 'password_2')}
#          ),
#     )
#     search_fields: List[str] = ['email']
#     # ordering = [created_at] #// have to fix this -> can not find created_at that is from BaseModel.
#     list_per_page = 10
#     filter_horizontal: Tuple = ()
#     actions = [export_to_csv]


# admin.site.register(User, CustomUserAdmin)



class AddressInline(admin.StackedInline):
    model = Address
    can_delete = True
    verbose_plural_name = "Addresses"
    fk_name = 'customer'
    extra = 1