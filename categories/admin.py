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
    list_filter = ['name']

    fieldsets = (
        ('Data fields', { 'fields': ('name', 'category_image') }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'category_image')
        })
    )

    ordering = ['name']
    filter_horizontal = ()

admin.site.register(Category, CustomCategoryAdmin)
