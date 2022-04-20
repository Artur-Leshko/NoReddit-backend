from rest_framework import permissions, serializers
from rest_framework.decorators import action

from api.viewsets import CreateRetrieveUpdateDestroyViewset
from api.permissions import IsCommentOwner, IsCommentOwnerOrPostOwner
from api.exeptions import CustomApiException

from userprofile.models import UserProfile
from comments.models import Comment
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
