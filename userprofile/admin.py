from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AdminUpdateForm, AdminCreationForm

admin.site.unregister(Group)

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    '''
        Admin view of user
    '''

    form = AdminCreationForm
    add_form = AdminUpdateForm

    list_display = ['username', 'email', 'firstname', 'surname', 'is_staff', 'is_active']
    list_filter = ['username', 'email', 'is_staff', 'is_active']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
