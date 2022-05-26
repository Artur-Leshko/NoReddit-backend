from rest_framework import permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.viewsets import CreateRetrieveUpdateDestroyViewset
from api.permissions import IsCommentOwner, IsCommentOwnerOrPostOwner
from api.exeptions import CustomApiException

from userprofile.models import UserProfile
from comments.models import Comment, CommentVote
from .serializers import CommentSerializer, CommentCreateSerializer

QUERY_STRING_FOR_VOTED_COMMENTS = '''
    SELECT cc.id, cc.text, cc.owner_id, cc.post_id, cc.created_at, cc.updated_at
        FROM comments_comment cc
            INNER JOIN comments_commentvote cv ON cc.id = cv.comment_id
                AND cv.vote_type = %s
			INNER JOIN userprofile_userprofile uu ON uu.id = cv.owner_id
				AND uu.id = %s
        WHERE cc.post_id = %s
    GROUP BY cc.id
    ORDER BY cc.created_at DESC
'''

class CommentPagination(PageNumberPagination):
    '''
        Number of comments for pagination
    '''
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000

class CommentView(CreateRetrieveUpdateDestroyViewset):
    '''
        CRUD for comments
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_by_action = {
        'update': [IsCommentOwner],
        'destroy': [IsCommentOwnerOrPostOwner],
    }
    pagination_class = CommentPagination

    def create(self, request, *args, **kwargs):
        '''
            creating comment
        '''
        self.serializer_class = CommentCreateSerializer
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request!")

    def update(self, request, *args, **kwargs):
        '''
            updating comment
        '''
        try:
            kwargs.update({'partial': True})
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request!")

    def perform_create(self, serializer):
        '''
            performing creation of the comment
        '''
        serializer.save(owner=UserProfile.objects.get(pk=self.request.user.id))

    @action(methods=['put'], detail=True, url_path='upvote', permission_classes=[permissions.IsAuthenticated])
    def upvote(self, *args, **kwargs):
        '''
            upvoting comment
        '''
        comment_id = kwargs.get('pk')
        comment_vote = CommentVote.objects.filter(owner=self.request.user.id, comment=comment_id)
        comment_vote_values = comment_vote.values()

        if not comment_vote:
            new_comment_vote = CommentVote.objects.create(owner=UserProfile.objects.get(pk=self.request.user.id),
                comment=Comment.objects.get(pk=comment_id), vote_type='up')
            new_comment_vote.save()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif comment_vote_values[0]['vote_type'] == 'down':
            comment_vote[0].vote_type = 'up'
            comment_vote[0].save()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comment_vote.delete()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True, url_path='downvote', permission_classes=[permissions.IsAuthenticated])
    def downvote(self, *args, **kwargs):
        '''
            downvoting comment
        '''
        comment_id = kwargs.get('pk')
        comment_vote = CommentVote.objects.filter(owner=self.request.user.id, comment=comment_id)
        comment_vote_values = comment_vote.values()

        if not comment_vote:
            new_comment_vote = CommentVote.objects.create(owner=UserProfile.objects.get(pk=self.request.user.id),
                comment=Comment.objects.get(pk=comment_id), vote_type='down')
            new_comment_vote.save()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif comment_vote_values[0]['vote_type'] == 'up':
            comment_vote[0].vote_type = 'down'
            comment_vote[0].save()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comment_vote.delete()

            serializer = CommentSerializer(self.get_object())

            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='upvoted', permission_classes=[permissions.IsAuthenticated])
    def upvoted_comments_list(self, *args, **kwargs):
        '''
            returns list of upvoted comments
        '''
        post_id = kwargs.get('pk')
        comments = Comment.objects.raw(QUERY_STRING_FOR_VOTED_COMMENTS, ['up', self.request.user.id, post_id])
        serializer = CommentSerializer(self.paginate_queryset(comments), many=True)

        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=True, url_path='downvoted', permission_classes=[permissions.IsAuthenticated])
    def downvoted_comments_list(self, *args, **kwargs):
        '''
            returns list of upvoted comments
        '''
        post_id = kwargs.get('pk')
        comments = Comment.objects.raw(QUERY_STRING_FOR_VOTED_COMMENTS, ['down', self.request.user.id, post_id])
        serializer = CommentSerializer(self.paginate_queryset(comments), many=True)

        return self.get_paginated_response(serializer.data)
