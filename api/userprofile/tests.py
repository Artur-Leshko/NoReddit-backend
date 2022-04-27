from re import S
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from .serializers import UserProfileSerializer, FollowerSerializer
from api.exeptions import CustomApiException

User = get_user_model()

class UserProfileTests(APITestCase):
    '''
        Tests for UserProfileview
    '''

    def setUp(self):
        '''
            function that set ups database for tests
        '''

        self.first_user = User.objects.create_user(username='my user',
            email='abcdf@mail.ru', password='qwe123')
        self.first_user.save()

        self.second_user = User.objects.create_user(username='my second user',
            email='test.second@mail.ru', password='abcd1234')
        self.second_user.save()

        self.third_user = User.objects.create_user(username='my third user',
            email='test.third@mail.ru', password='abcd1234')
        self.third_user.save()

        self.first_userprofile = UserProfile.objects.create(user=self.first_user,
            id=self.first_user.id)
        self.first_userprofile.save()

        self.second_userprofile = UserProfile.objects.create(user=self.second_user,
            id=self.second_user.id, firstname='hello')
        self.second_userprofile.save()

        self.third_userprofile = UserProfile.objects.create(user=self.third_user,
            id=self.third_user.id)
        self.third_userprofile.save()

        self.first_user_token = AccessToken.for_user(self.first_user)
        self.third_user_token = AccessToken.for_user(self.third_user)

        self.first_userprofile.followers.add(self.second_userprofile)
        self.second_userprofile.followers.add(self.first_userprofile)
        self.third_userprofile.followers.add(self.first_userprofile)

    def test_valid_userprofile(self):
        '''
            tests that userprofile view returns info for logged-in user
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.get(reverse('userprofile'))
        serializer = UserProfileSerializer(UserProfile.objects.get(user=self.first_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_invalid_profile(self):
        '''
            tests that unauthorized user can not access the userprofile data
        '''
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_delete_profile(self):
        '''
            tests that authorized user can delete his profile
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.delete(reverse('userprofile'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            self.first_user.refresh_from_db()
        except User.DoesNotExist:
            self.assertRaises(User.DoesNotExist)

    def test_unauthorized_delete_profile(self):
        '''
            tests that unauthorized user can not delete profile
        '''
        response = self.client.delete(reverse('userprofile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_valid_update_profile(self):
        '''
            tests that authorized user can update his profile with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.put(reverse('userprofile'), { 'firstname': 'my name',
            'surname': 'lalala' })
        self.first_userprofile.refresh_from_db()
        serializer = UserProfileSerializer(self.first_userprofile)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.json(), serializer.data)

    def test_authorized_invalid_update_profile(self):
        '''
            tests that authorized user can not update his profile with invalid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.put(reverse('userprofile'), { 'firstname': 'my name',
            'user': { 'username': '' } })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unauthorized_update_profile(self):
        '''
            test that unauthorized user can not update profile (second user)
        '''
        response = self.client.put(reverse('userprofile'), { 'firstname': 'hi' })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        old_firstname = self.second_userprofile.firstname
        self.second_userprofile.refresh_from_db()
        self.assertEqual(self.second_userprofile.firstname, old_firstname)

    def test_valid_public_profile(self):
        '''
            tests that authorized user can get info about any userprofile
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.get(reverse('userprofile_public',
            kwargs={"pk": self.second_user.id}))
        serializer = UserProfileSerializer(UserProfile.objects.get(user=self.second_user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_invalid_public_profile(self):
        '''
            test that unauthorized user can not access userprofile info of different users
        '''
        response = self.client.get(reverse('userprofile_public',
            kwargs={"pk": self.second_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_registration(self):
        '''
            tests registration with valid data
        '''
        response = self.client.post(reverse('user_registration'), {'username': 'clear',
            'email': 'gfdh@mail.ru', 'password': 'asdfgh'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration(self):
        '''
            tests registration with invalid data
        '''
        with self.assertRaises(CustomApiException):
            self.client.post(reverse('user_registration'), {'username': 'clear',
                'password': 'asdfg'})

    def test_exist_user_registration(self):
        '''
            tests registration of user with already existing data
        '''
        with self.assertRaises(CustomApiException):
            self.client.post(reverse('user_registration'), {'username': 'my user',
                'email': 'abcdf@mail.ru', 'password': 'qwe123'})

    def test_authorized_subscription(self):
        '''
            authorized user can subscribe on another user
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.post(reverse('userprofile_subscribe',
            kwargs={"pk": self.second_userprofile.id}))

        self.third_userprofile.refresh_from_db()
        serializer = UserProfileSerializer(self.third_userprofile)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.json().get('followed_count'), 2)
        self.assertEqual(response.json().get('followed_count'), serializer.data.get('followed_count'))

    def test_unauthorized_subscription(self):
        '''
            unauthorized user can't subscribe on another user
        '''
        response = self.client.post(reverse('userprofile_subscribe',
            kwargs={"pk": self.second_userprofile.id}))

        self.third_userprofile.refresh_from_db()
        serializer = UserProfileSerializer(self.third_userprofile)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(serializer.data.get('followed_count'), 1)

    def test_self_subscription(self):
        '''
            user can't subscribe on himself
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.post(reverse('userprofile_subscribe',
            kwargs={"pk": self.third_userprofile.id}))

        self.third_userprofile.refresh_from_db()
        serializer = UserProfileSerializer(self.third_userprofile)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('message'), "You can not subscribe on yourself!")
        self.assertEqual(serializer.data.get('followed_count'), 1)

    def test_authorized_unsubscribe(self):
        '''
            authorized user can unsubscribe from another user
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.post(reverse('userprofile_unsubscribe',
            kwargs={"pk": self.first_userprofile.id}))

        self.first_userprofile.refresh_from_db()
        self.third_userprofile.refresh_from_db()

        first_user_serializer = UserProfileSerializer(self.first_userprofile)
        third_user_serializer = UserProfileSerializer(self.third_userprofile)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), third_user_serializer.data)
        self.assertEqual(first_user_serializer.data.get('followers_count'), 1)
        self.assertEqual(third_user_serializer.data.get('followed_count'), 0)

    def test_unauthorized_unsubscribe(self):
        '''
            unauthorized user can't unsubscribe from another user
        '''
        response = self.client.post(reverse('userprofile_unsubscribe',
            kwargs={"pk": self.first_userprofile.id}))

        self.first_userprofile.refresh_from_db()
        self.third_userprofile.refresh_from_db()
        first_user_serializer = UserProfileSerializer(self.first_userprofile)
        third_user_serializer = UserProfileSerializer(self.third_userprofile)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(first_user_serializer.data.get('followers_count'), 2)
        self.assertEqual(third_user_serializer.data.get('followed_count'), 1)
