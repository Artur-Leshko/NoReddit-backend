import mock
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
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


        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'photo.jpg'

        self.first_category = Category.objects.create(name="Fun",
            description="Some funny jokes here", category_image=self.file_mock.name)
        self.second_category = Category.objects.create(name="Tech",
            description="Something about technologies", category_image=self.file_mock.name)


        file_image = self.get_image_file()

        self.data = {
            'name': '123',
            'description': 'adsasdasdasdasd',
            'category_image': file_image
        }

        self.invalid_data = {
            'description': 'adsasdasdasdasd',
            'category_image': file_image
        }

        self.edit_data = {
            'name': 'Jokes'
        }

        self.edit_invalid_data = {
            'name': ''
        }

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        '''
            creates image object
        '''
        image = BytesIO()
        Image.new("RGB", size=size, color=color).save(image, ext)
        image.seek(0)

        return SimpleUploadedFile(name, image.getvalue())

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

    def test_authorized_category_detail(self):
        '''
            every authorized user can get category details
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.get(reverse('category_detail',
            kwargs={"pk": self.first_category.id}
        ))

        serializer = CategoryDetailSerializer(self.first_category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('id'), serializer.data.get('id'))

    def test_unauthorized_category_detail(self):
        '''
            unauthorized user can't get category details
        '''
        response = self.client.get(reverse('category_detail',
            kwargs={"pk": self.first_category.id}
        ))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_admin_valid_category_create(self):
        '''
            admin can create new categories with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.post(reverse('category_create'), self.data, format='multipart')

        serializer = CategorySerializer(Category.objects.get(name='123'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('id'), serializer.data.get('id'))


    def test_admin_invalid_category_create(self):
        '''
            admin can't create new categories with invalid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.post(reverse('category_create'), self.invalid_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_category_create(self):
        '''
            user can't create new categories
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.post(reverse('category_create'), self.data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_category_create(self):
        '''
            unauthorized user can't create new categories
        '''
        response = self.client.post(reverse('category_create'), self.data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_valid_category_edit(self):
        '''
            admin can change category data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.put(reverse('category_edit',
            kwargs={"pk": self.first_category.id}), self.edit_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.first_category.name, "Jokes")

    def test_admin_invalid_category_edit(self):
        '''
            admin can't change category data
        '''
        old_category = self.first_category

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.put(reverse('category_edit',
            kwargs={"pk": self.first_category.id}), self.edit_invalid_data, format='multipart')

        self.first_category.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(old_category, self.first_category)

    def test_user_category_edit(self):
        '''
            user can't change category data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.put(reverse('category_edit',
            kwargs={"pk": self.first_category.id}), self.edit_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_category_edit(self):
        '''
            unauthorized user can't change category data
        '''
        response = self.client.put(reverse('category_edit',
            kwargs={"pk": self.first_category.id}), self.edit_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

