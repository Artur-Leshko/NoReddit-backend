from django import forms
from .models import Category

class AdminCreationCategoryForm(forms.ModelForm):
    '''
        Admin form for creating category
    '''

class AdminUpdateCategoryForm(forms.ModelForm):
    '''
        Admin form for updateing category
    '''

