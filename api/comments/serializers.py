from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.exeptions import CustomApiException

from comments.models import Comment
from posts.models import Post
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
        fields = ['id', 'text', 'comment_owner', 'post', 'created_at', 'updated_at']
        read_only_fields = ['id', 'comment_owner', 'post', 'craeted_at', 'updated_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    '''
        Serializer for comment creation
    '''
    post = PostCommentSerializer(read_only=True, required=False)
    owner = UserProfileReadSerializer(read_only=True, required=False)
    post_id = serializers.UUIDField(write_only=True)

    class Meta:
        '''
            Meat class for CommentCreateSerializer
        '''
        model = Comment
        fields = ['id', 'text', 'post', 'owner', 'post_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            post_id = validated_data.pop('post_id')
            post = get_object_or_404(Post, id=post_id)
            validated_data.update({'post': post})
            instance = Comment.objects.create(**validated_data)
        except Post.DoesNotExist:
            raise CustomApiException(400, "Post with this id does not exist!")

        return instance
