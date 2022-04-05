from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from posts.models import Post, Vote
from .serializers import PostSerializer, CreatePostSerializer
from api.exeptions import CustomApiException

User = get_user_model()

# path('popular/', views.PopularPostsList.as_view(), name='posts_popular'),

# path('<str:pk>/upvote/', views.UpvotePostDetail.as_view(), name='post_upvote'),
# path('<str:pk>/downvote/', views.DownvotePostDetail.as_view(), name='post_downvote'),

# path('<str:pk>/delete/', views.DestroyPostView.as_view(), name='post_delete'),
# path('<str:pk>/edit/', views.UpdatePostView.as_view(), name='post_edit'),

class PostsAndVotesTests(APITestCase):
    '''
        Tests for Posts and Votes
    '''

    def setUp(self):
        '''
            set ups database for tests
        '''

        self.first_user = User.objects.create_user(username='my user',
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

        self.third_user = User.objects.create_user(username='my third user',
            email='klmn@mail.ru', password='qwe123')
        self.third_user.save()
        self.third_userprofile = UserProfile.objects.create(user=self.third_user,
            id=self.third_user.id)
        self.third_userprofile.save()

        self.first_user_token = AccessToken.for_user(self.first_user)
        self.second_user_token = AccessToken.for_user(self.second_user)
        self.third_user_token = AccessToken.for_user(self.third_user)

        self.first_user_post = Post.objects.create(owner=self.firt_userprofile,
            title="First user post", main_text="Qwe rty")
        self.first_user_post.save()

    def test_authorized_valid_post_creation(self):
        '''
            authorized user can create new post with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.post(reverse('posts_create'), {'title': 'Second user post',
            'main_text': 'asdasdasd'})

        serializer = CreatePostSerializer(Post.objects.get(title='Second user post'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serializer.data)

    def test_authorized_invalid_post_creation(self):
        '''
            authorized user can't create new post with invalid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))

        without_title_response = self.client.post(reverse('posts_create'), {'main_text': 'ad'})
        without_text_response = self.client.post(reverse('posts_create'), {'title': 'ad'})
        empty_response = self.client.post(reverse('posts_create'), {})
        blank_title_response = self.client.post(reverse('posts_create'), {'title': '',
            'main_text': 'asds'})
        blank_text_response = self.client.post(reverse('posts_create'), {'title': 'asd',
            'main_text': ''})

        self.assertEqual(without_title_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(without_text_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(empty_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(blank_text_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(blank_title_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_post_creation(self):
        '''
            unauthorized user can't create new post
        '''
        response = self.client.post(reverse('posts_create'), {'title': 'ad',
            'main_text': 'asdsad'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authorized_post_details(self):
        '''
            authorized user can watch the post
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        first_response = self.client.get(reverse('post_show',
            kwargs={"pk": self.first_user_post.id}))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        second_response = self.client.get(reverse('post_show',
            kwargs={"pk": self.first_user_post.id}))

        serializer = PostSerializer(self.first_user_post)

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_response.json(), serializer.data)

        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.json(), serializer.data)

    def test_unauthorized_post_details(self):
        '''
            unauthorized user can't watch the post
        '''
        response = self.client.get(reverse('post_show',
            kwargs={"pk": self.first_user_post.id}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_post_owner_delete(self):
        '''
            authorized post owner can delete the post
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.delete(reverse('post_delete',
            kwargs={"pk": self.first_user_post.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            self.first_user_post.refresh_from_db()
        except Post.DoesNotExist:
            self.assertRaises(Post.DoesNotExist)


    def test_authorized_post_delete(self):
        '''
            authorized user can't delete the post of another user
        '''
        old_first_user_post = self.first_user_post

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.delete(reverse('post_delete',
            kwargs={"pk": self.first_user_post.id}))

        self.first_user_post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_first_user_post, self.first_user_post)

    def test_unauthorized_post_delete(self):
        '''
            unauthorized user can't delete the post
        '''
        response = self.client.delete(reverse('post_delete',
            kwargs={"pk": self.first_user_post.id}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
