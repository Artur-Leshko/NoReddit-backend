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
    queryset = Post.objects.all()
