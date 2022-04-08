from rest_framework import serializers

from api.userprofile.serializers import UserProfilePostSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfilePostSerializer()

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['id', 'owner', 'title', 'main_text', 'upvotes', 'downvotes']
        read_only_fields = ['id', 'owner', 'upvotes', 'downvotes']


class CreatePostSerializer(serializers.ModelSerializer):
    '''
        Serializer for creating Post model
    '''

    class Meta:
        '''
            Meta class for CreatePostSerializer
        '''
        model = Post
        fields = ['id', 'title', 'main_text']
