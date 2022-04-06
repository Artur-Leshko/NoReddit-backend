from datetime import timedelta
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.exeptions import CustomApiException
from api.permissions import IsPostOwner
from userprofile.models import UserProfile
from posts.models import Post, Vote
from .serializers import PostSerializer, CreatePostSerializer

class PostPagination(PageNumberPagination):
    '''
        Number of posts for pagiantion
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PopularPostsList(generics.ListAPIView):
    '''
        Posts list for main page
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination
    queryset = Post.objects.all()
    # Q(created_at=timedelta(days=3) & Q(votes__gte=50) | Q(created_at=timedelta(days=1)))

class CreatePost(generics.CreateAPIView):
    '''
        Creating post
    '''
    serializer_class = CreatePostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=UserProfile.objects.get(pk=self.request.user.id))

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request")

class UpvotePostDetail(APIView):
    '''
        Upvotes and returns renewed Post
    '''
    permisson_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        '''
            returns Post object
        '''
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise CustomApiException(404, 'This post does not exist!')

        return post

    def put(self, request, pk):
        '''
            Add or delete upvote from post
        '''

        current_vote = Vote.objects.filter(owner=request.user.id, post=pk)
        current_vote_values = current_vote.values()

        if not current_vote:
            new_vote = Vote.objects.create(owner=UserProfile.objects.get(pk=request.user.id),
                post=Post.objects.get(pk=pk), vote_type='up')
            new_vote.save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif current_vote_values[0]['vote_type'] == 'down':
            current_vote[0].vote_type = 'up'
            current_vote[0].save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            current_vote.delete()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


class DownvotePostDetail(APIView):
    '''
        Downvotes and returns renewed post
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        '''
            returns Post object
        '''

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise CustomApiException(404, 'This post does not exist!')
        return post

    def put(self, request, pk):
        '''
            Add or delete downote for post
        '''

        current_vote = Vote.objects.filter(owner=request.user.id, post=pk)
        current_vote_values = current_vote.values()

        if not current_vote:
            new_vote = Vote.objects.create(owner=UserProfile.objects.get(pk=request.user.id),
                post=Post.objects.get(pk=pk), vote_type='down')
            new_vote.save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif current_vote_values[0]['vote_type'] == 'up':
            current_vote[0].vote_type = 'down'
            current_vote[0].save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            current_vote.delete()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


class RetrievePostView(generics.RetrieveAPIView):
    '''
        View for showing post
    '''

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class DestroyPostView(generics.DestroyAPIView):
    '''
        View for deleting post
    '''
    permission_classes = [IsPostOwner]
    queryset = Post.objects.all()

class UpdatePostView(generics.UpdateAPIView):
    '''
        View for updating post
    '''
    permission_classes = [IsPostOwner]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def put(self, request, *args, **kwargs):
        try:
            return self.partial_update(request, *args, **kwargs)
        except serializers.ValidationError:
            raise CustomApiException(400, "Bad request!")
