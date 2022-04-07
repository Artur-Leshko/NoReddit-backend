from rest_framework import serializers

from api.userprofile.serializers import UserProfileSerializer
from posts.models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfileSerializer()
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['id', 'owner', 'title', 'main_text', 'upvotes', 'downvotes']
        read_only_fields = ['id', 'owner', 'upvotes', 'downvotes']

    def get_upvotes(self, obj):
        '''
            returns count of upvotes for post
        '''
        return Vote.objects.filter(post=obj.id, vote_type='up').count()

    def get_downvotes(self, obj):
        '''
            returns count of downvotes for post
        '''
        return Vote.objects.filter(post=obj.id, vote_type='down').count()


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
