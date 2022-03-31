from  datetime import timedelta
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework import generics

from posts.models import Post
from .serializers import PostSerializer

class PopularPostsList(generics.ListAPIView):
    '''
        Posts list for main page
    '''
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.filter(Q(created_at=timedelta(days=3) & Q(votes__gte=50) | Q(created_at=timedelta(days=1))))
