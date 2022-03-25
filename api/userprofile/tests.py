from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from userprofile.models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()


class UserProfileTests(APITestCase):
    '''
        Tests for UserProfileview
    '''

    def setUp(self):
        '''
            function that set ups database for tests
        '''
