from django import forms
from .models import Category

class AdminCategoryForm(forms.ModelForm):
    '''
        Admin form for updateing category
    '''

    class Meta:
        '''
            Meta class for AdminUpdateCategoryForm
        '''
        model = Category
        fields = ['id', 'name', 'description', 'category_image']

    def clean(self):
        cleaned_data = super().clean()

        category_description = cleaned_data.get('description')

        if not category_description or len(category_description) < 10:
            self.add_error('description', 'Description should consist of at least 10 simbols!')
