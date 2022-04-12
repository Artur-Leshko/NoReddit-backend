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
        fields = ['id', 'name', 'category_image']
        read_only_fields = ['id', 'name', 'category_image']
