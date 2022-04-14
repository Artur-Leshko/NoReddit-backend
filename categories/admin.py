from django.contrib import admin

from .models import Category
from .forms import AdminCategoryForm

class CustomCategoryAdmin(admin.ModelAdmin):
    '''
        Admin view of Category
    '''

    form = AdminCategoryForm

    list_display = ['id', 'name']
    list_filter = ['created_at']

    fieldsets = (
        ('Data fields', { 'fields': ('name', 'description', 'category_image') }),
    )

    ordering = ['name']

admin.site.register(Category, CustomCategoryAdmin)
