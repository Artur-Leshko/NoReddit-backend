import uuid
from django.db import models
from posts.models import Post

def category_path(instance, filename):
    '''
        makes path of the file using category id
    '''
    splited_filename = str(filename).split('.')
    image_name = str(uuid.uuid4()) + '.' + splited_filename[-1]
    return 'category/{0}/{1}'.format(instance.id, image_name)


class Category(models.Model):
    '''
        Model for Category
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=False, unique=True)
    category_image = models.ImageField(upload_to=category_path, blank=False, null=False)
    posts = models.ManyToManyField(Post)
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

    @property
    def posts_count(self):
        '''
            returns count of posts that related with particular category
        '''
        return Post.objects.filter(category__id=self.id).count()
