from django import forms
from .models import Category

class AdminCreationCategoryForm(forms.ModelForm):
    '''
        Admin form for creating category
    '''

    class Meta:
        '''
            Meta class for AdminCreationCategoryForm
        '''
        model = Category
        fields = ['name', 'category_image']

    def clean(self):
        cleaned_data = super().clean()

        category_name = cleaned_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            self.add_error('name', 'Category with this name already exists!')


class AdminUpdateCategoryForm(forms.ModelForm):
    '''
        Admin form for updateing category
    '''

    class Meta:
        '''
            Meta class for AdminUpdateCategoryForm
        '''
        model = Category
        fields = ['name', 'category_image']

    def clean(self):
        cleaned_data = super().clean()

        category_name = cleaned_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            self.add_error('name', 'Category with this name already exests!')
