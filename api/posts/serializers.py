from django.db.models import Q
from rest_framework import serializers

from api.userprofile.serializers import UserProfileSerializer
from posts.models import Post, Vote


class VoteSerializer(serializers.ModelSerializer):
    '''
        Serializer for Vote model
    '''

    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()

    class Meta:
        '''
            Meta class for VoteSerializer
        '''
        model = Vote
        fields = ['upvotes', 'downvotes']

    def get_upvotes(self):
        '''
            returns count of upvotes for post
        '''
        return Vote.objects.filter(Q(owner=self.context['request'].user.id) &
            Q(vote_type='up')).count()

    def get_downvotes(self):
        '''
            returns count of downvotes for post
        '''
        return Vote.objects.filter(Q(owner=self.context['request'].user.id) &
            Q(vote_type='down')).count()


class PostSerializer(serializers.ModelSerializer):
    '''
        Serializer for Post model
    '''

    owner = UserProfileSerializer(many=False)
    owner = serializers.ReadOnlyField()

    votes = VoteSerializer(many=True)

    class Meta:
        '''
            Meta class for PostSerializer
        '''
        model = Post
        fields = ['owner', 'title', 'main_text', 'votes']
