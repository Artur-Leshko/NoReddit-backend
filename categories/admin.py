from django.contrib import admin

from .models import Category
from .forms import AdminCreationCategoryForm, AdminUpdateCategoryForm

class CustomCategoryAdmin(admin.ModelAdmin):
    '''
        Admin view of Category
    '''

    form = AdminUpdateCategoryForm
    add_form = AdminCreationCategoryForm

    list_display = ['id', 'name']
    list_filter = ['created_at']

    fieldsets = (
        ('ID field', { 'fields': ('id',) }),
        ('Data fields', { 'fields': ('name', 'description', 'category_image') })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description', 'category_image')
        })
    )

    ordering = ['name']
    filter_horizontal = ()

admin.site.register(Category, CustomCategoryAdmin)
