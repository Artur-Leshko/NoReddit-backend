from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile
from .forms import AdminUpdateForm, AdminCreationForm

admin.site.unregister(Group)

User = get_user_model()

class CustomUserAdmin(BaseUserAdmin):
    '''
        Admin view of user
    '''

    form = AdminUpdateForm
    add_form = AdminCreationForm

    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

    fieldsets = (
        (None, { 'fields': ('email', 'username', 'password') }),
        ('Permissions', { 'fields': ('is_staff', 'is_admin', 'is_active') })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password_confirmation', 'is_staff', 'is_admin')
        }),
    )

    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
