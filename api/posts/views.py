from rest_framework import permissions, status, filters
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.db.models import Count

from api.exeptions import CustomApiException
from api.permissions import IsPostOwner
from userprofile.models import UserProfile
from posts.models import Post, Vote
from comments.models import Comment
from api.comments.serializers import CommentSerializer
from .serializers import PostSerializer, CreatePostSerializer

QUERY_STRING_FOR_POPULAR_POSTS = '''
    SELECT pp.id, pp.title, pp.main_text, pp.owner_id, COUNT(pv) AS UpvotesCount
        FROM posts_post pp
            INNER JOIN posts_vote pv ON pp.id = pv.post_id
                AND pv.vote_type = 'up'
                AND pp.created_at >= NOW() - INTERVAL '10 DAY'
    GROUP BY pp.id
    HAVING COUNT(pv.vote_type='up')>=2
    ORDER BY pp.created_at {0}
'''

QUERY_STRING_FOR_VOTED_POSTS = '''
    SELECT pp.id, pp.title, pp.main_text, pp.owner_id
        FROM posts_post pp
            INNER JOIN posts_vote pv ON pp.id = pv.post_id
                AND pv.vote_type = %s
			INNER JOIN userprofile_userprofile uu ON uu.id = pv.owner_id
				AND uu.id = %s
    GROUP BY pp.id
    ORDER BY pp.created_at DESC
'''

class PostPagination(PageNumberPagination):
    '''
        Number of posts for pagiantion
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CommentPagination(PageNumberPagination):
    '''
        Number of comments for pagination
    '''
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PopularPostsList(generics.ListAPIView):
    '''
        Posts list for main page
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination
    queryset = Post.objects.all()

    def get_queryset(self):
        order = self.request.query_params.get('ordering')
        posts = Post.objects.raw(QUERY_STRING_FOR_POPULAR_POSTS.format(order or 'DESC'))

        return posts

class ListPosts(generics.ListAPIView):
    '''
        returns list of posts
    '''
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', '^owner__user__username', 'owner__user__id']
    ordering_fields = ['title', 'owner__user__username', 'created_at']
    ordering = ['-created_at']

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif current_vote_values[0]['vote_type'] == 'down':
            current_vote[0].vote_type = 'up'
            current_vote[0].save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            current_vote.delete()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_200_OK)


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

        # try:
        if not current_vote:
            new_vote = Vote.objects.create(owner=UserProfile.objects.get(pk=request.user.id),
                post=Post.objects.get(pk=pk), vote_type='down')
            new_vote.save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif current_vote_values[0]['vote_type'] == 'up':
            current_vote[0].vote_type = 'down'
            current_vote[0].save()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            current_vote.delete()

            serializer = PostSerializer(self.get_object(pk))

            return Response(serializer.data, status=status.HTTP_200_OK)

class UpvotedUserPostListView(generics.ListAPIView):
    '''
        returns upvoted posts for current user
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PostPagination

    def get_queryset(self):
        posts = Post.objects.raw(QUERY_STRING_FOR_VOTED_POSTS, ['up', self.request.user.id])

        return posts


class DownvotedUserPostListView(generics.ListAPIView):
    '''
        returns downvoted posts for current user
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PostPagination

    def get_queryset(self):
        posts = Post.objects.raw(QUERY_STRING_FOR_VOTED_POSTS, ['down', self.request.user.id])

        return posts

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


class PostCommentsList(generics.ListAPIView):
    '''
        returns list of post comments
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        comments = Comment.objects.filter(post=self.kwargs.get('pk'))

        return comments.annotate(Count('commentvote')).order_by('-commentvote__count')
