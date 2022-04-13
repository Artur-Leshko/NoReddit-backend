from rest_framework import serializers

from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    '''
        Serializer for Category model
    '''

    class Meta:
        '''
            Meta class for CategorySerializer
        '''
        model = Category
        fields = ['id', 'name', 'description', 'category_image']
        read_only_fields = ['id', 'name', 'description', 'category_image']

class CategoryDetailSerializer(serializers.ModelSerializer):
    '''
        Serializer for category detail view
    '''

    class Meta:
        '''
            Meta class for CategoryDetailSerializer
        '''
        model = Category
        fields = ['id', 'name', 'description', 'category_image', 'posts_count']
        read_only_fields = ['id', 'name', 'description', 'category_image', 'posts_count']
