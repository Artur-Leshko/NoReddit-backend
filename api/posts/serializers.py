from rest_framework import serializers
from api.userprofile.serializers import UserProfileSerializer
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfileSerializer(many=False)
    owner = serializers.ReadOnlyField()

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['owner', 'title', 'main_text']

