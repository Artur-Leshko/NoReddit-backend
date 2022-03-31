from  datetime import timedelta
from django.db.models import Q
from rest_framework import permissions
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from posts.models import Post
from .serializers import PostSerializer

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
    queryset = Post.objects.filter(Q(created_at=timedelta(days=3) & Q(votes__gte=50) | Q(created_at=timedelta(days=1))))
