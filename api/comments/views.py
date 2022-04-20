from rest_framework import permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.viewsets import CreateRetrieveUpdateDestroyViewset
from api.permissions import IsCommentOwner, IsCommentOwnerOrPostOwner
from api.exeptions import CustomApiException

from userprofile.models import UserProfile
from comments.models import Comment, CommentVote
from .serializers import CommentSerializer, CommentCreateSerializer

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

    def create(self, request, *args, **kwargs):
        '''
            creating comment
        '''
        self.serializer_class = CommentCreateSerializer
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as exc:
            print(exc.detail)
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

    @action(methods=['put'], detail=True, url_path='upvote')
    def upvote(self, *args, **kwargs):
        '''
            upvoting comment
        '''
        comment_id = kwargs.get('pk')
        comment_vote = CommentVote.objects.filter(owner=self.request.user.id, comment=comment_id)
        comment_vote_values = comment_vote.values()

        if not comment_vote:
            new_comment_vote = CommentVote.objects.create(owner=UserProfile.objects.get(pk=self.request.user.id,
                comment=Comment.objects.get(pk=comment_id), vote_type='up'))
            new_comment_vote.save()

            serializer = CommentSerializer(self.get_object(comment_id))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif comment_vote_values[0]['vote_type'] == 'down':
            comment_vote[0].vote_type = 'up'
            comment_vote[0].save()

            serializer = CommentSerializer(self.get_object(comment_id))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            comment_vote.delete()

            serializer = CommentSerializer(self.get_object(comment_id))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
