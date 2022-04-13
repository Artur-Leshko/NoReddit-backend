from rest_framework import serializers

from api.userprofile.serializers import UserProfilePostSerializer
from api.categories.serializers import CategorySerializer
from posts.models import Post
from categories.models import Category


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfilePostSerializer()
    categories = serializers.ListSerializer(child=CategorySerializer())

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['id', 'owner', 'title', 'main_text', 'upvotes', 'downvotes', 'categories']
        read_only_fields = ['id', 'owner', 'upvotes', 'downvotes']


class CreatePostSerializer(serializers.ModelSerializer):
    '''
        Serializer for creating Post model
    '''

    categories = serializers.ListSerializer(child=CategorySerializer())

    class Meta:
        '''
            Meta class for CreatePostSerializer
        '''
        model = Post
        fields = ['id', 'title', 'main_text', 'categories']

    def create(self, validated_data):
        validated_data.pop('categories')
        instance = Post.objects.create(**validated_data)
        instance.save()

        for index, value in enumerate(self.initial_data.get('categories')):
            instance.category_set.add(Category.objects.get(id=value.get('id')))

        return instance
