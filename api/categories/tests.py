import mock
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files import File
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

        self.first_user = User.objects.create_superuser(username='my user',
            email='abcdf@mail.ru', password='qwe123')
        self.first_user.save()
        self.firt_userprofile = UserProfile.objects.create(user=self.first_user,
            id=self.first_user.id)
        self.firt_userprofile.save()

        self.second_user = User.objects.create_user(username='my second user',
            email='beee@mail.ru', password='qwe123')
        self.second_user.save()
        self.second_userprofile = UserProfile.objects.create(user=self.second_user,
            id=self.second_user.id)
        self.second_userprofile.save()


        self.first_user_token = AccessToken.for_user(self.first_user)
        self.second_user_token = AccessToken.for_user(self.second_user)


        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'photo.jpg'

        self.first_category = Category.objects.create(name="Fun",
            description="Some funny jokes here", category_image=file_mock.name)
        self.second_category = Category.objects.create(name="Tech",
            description="Something about technologies", category_image=file_mock.name)


    def test_authorized_category_list(self):
        '''
            every authorized user can get all categories
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.get(reverse('categories_list'))

        first_serializer = CategorySerializer(self.first_category)
        second_serializer = CategorySerializer(self.second_category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('id'), first_serializer.data.get('id'))
        self.assertEqual(response.json()[1].get('id'), second_serializer.data.get('id'))

    def test_unauthorized_category_list(self):
        '''
            unauthorized user can't get all categories
        '''
        response = self.client.get(reverse('categories_list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
