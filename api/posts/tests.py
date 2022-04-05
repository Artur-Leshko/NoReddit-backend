from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from .serializers import PostSerializer, CreatePostSerializer
from api.exeptions import CustomApiException

User = get_user_model()

class PostsAndVotesTests(APITestCase):
    '''
        Tests for Posts and Votes
    '''

    def setUp(self):
        '''
            set ups database for tests
        '''
