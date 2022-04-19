from rest_framework import serializers

from comments.models import Comment
from api.userprofile.serializers import UserProfileReadSerializer
from api.posts.serializers import PostCommentSerializer

class CommentSerializer(serializers.ModelSerializer):
    '''
        serializer for Comment model
    '''

    comment_owner = UserProfileReadSerializer(many=False)
    post = PostCommentSerializer(many=False)

    class Meta:
        '''
            Meta class for CommentSerializer
        '''
        model = Comment
        fields = ['id', 'text', 'comment_owner', 'post', 'created_at', 'update_at']
        read_only_fields = ['id', 'comment_owner', 'post', 'craeted_at', 'update_at']
