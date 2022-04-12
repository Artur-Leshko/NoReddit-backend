import uuid
from django.db import models
from posts.models import Post

def category_path():
    '''
        makes path of the file using category id
    '''

class Category(models.Model):
    '''
        Model for Category
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=False)
    category_image = models.ImageField(upload_to=category_path, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for Category model
        '''
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
