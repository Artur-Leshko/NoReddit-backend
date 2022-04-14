from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from categories.models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer

User = get_user_model()

class CategoriesTests(APITestCase):
    '''
        Tests for Categories
    '''

    def setUp(self):
        '''
            set ups database for tests
        '''
