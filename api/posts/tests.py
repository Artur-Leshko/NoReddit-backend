from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from posts.models import Post, Vote
from comments.models import Comment
from api.comments.serializers import CommentSerializer
from .serializers import PostSerializer, CreatePostSerializer

User = get_user_model()

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

        self.second_user_post = Post.objects.create(owner=self.second_userprofile,
            title="Second user post", main_text="Qwe rty")
        self.second_user_post.save()

        self.third_user_post = Post.objects.create(owner=self.third_userprofile,
            title="Third user test post", main_text="Qwe rty")
        self.third_user_post.save()

        self.first_user_first_post_vote = Vote.objects.create(owner=self.firt_userprofile,
            post=self.first_user_post, vote_type='up')
        self.first_user_first_post_vote.save()
        self.second_user_first_post_vote = Vote.objects.create(owner=self.second_userprofile,
            post=self.first_user_post, vote_type='up')
        self.second_user_first_post_vote.save()
        self.third_user_first_post_vote = Vote.objects.create(owner=self.third_userprofile,
            post=self.first_user_post, vote_type='up')
        self.third_user_first_post_vote.save()

        self.first_user_second_post_vote = Vote.objects.create(owner=self.firt_userprofile,
            post=self.second_user_post, vote_type='up')
        self.first_user_second_post_vote.save()
        self.second_user_second_post_vote = Vote.objects.create(owner=self.second_userprofile,
            post=self.second_user_post, vote_type='up')
        self.second_user_second_post_vote.save()
        self.third_user_second_post_vote = Vote.objects.create(owner=self.third_userprofile,
            post=self.second_user_post, vote_type='down')
        self.third_user_second_post_vote.save()

        self.first_user_post_comment = Comment.objects.create(owner=self.firt_userprofile,
            post=self.first_user_post, text="XD")
        self.first_user_post_comment = Comment.objects.create(owner=self.second_userprofile,
            post=self.first_user_post, text="LOL")
        self.first_user_post_comment = Comment.objects.create(owner=self.third_userprofile,
            post=self.first_user_post, text="ROFL")


    def test_authorized_popular_post(self):
        '''
            authorized user can get popular posts
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.get(reverse('posts_popular'))

        serializer = PostSerializer(self.first_user_post)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), 1)
        self.assertEqual(response.json().get('results')[0], serializer.data)


    def test_unauthorized_popular_post(self):
        '''
            unauthorized user can't get popular posts
        '''
        response = self.client.get(reverse('posts_popular'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_valid_post_creation(self):
        '''
            authorized user can create new post with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.post(reverse('posts_create'), {'title': 'Third user post',
            'main_text': 'asdasdasd', 'categories': []})

        serializer = CreatePostSerializer(Post.objects.get(title='Third user post'))

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
            'main_text': 'asdsad', 'categories': []})
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

    def test_authorized_post_owner_valid_update(self):
        '''
            authorized post owner can update the post with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.first_user_post.id}), {'title': 'hello'})

        self.first_user_post.refresh_from_db()
        serializer = PostSerializer(self.first_user_post)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_authorized_post_owner_invalid_update(self):
        '''
            authorized post owner can't update the post with invalid data
        '''
        old_first_user_post = self.first_user_post
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))

        blank_title_response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.first_user_post.id}), {'title': ''})
        blank_text_response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.first_user_post.id}), {'main_text': ''})
        empty_response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.first_user_post.id}), {})

        self.first_user_post.refresh_from_db()

        self.assertEqual(blank_text_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(blank_title_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(empty_response.status_code, status.HTTP_200_OK)
        self.assertEqual(old_first_user_post, self.first_user_post)

    def test_authorized_post_update(self):
        '''
            authorized user can't update the post of another user
        '''
        old_first_user_post = self.first_user_post

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.first_user_post.id}), {'title': 'hello'})

        self.first_user_post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_first_user_post, self.first_user_post)

    def test_unauthorized_post_update(self):
        '''
            unauthorized user can't update the post
        '''
        old_third_user_post = self.third_user_post
        response = self.client.put(reverse('post_edit',
            kwargs={"pk": self.third_user_post.id}), {'title': 'hello'})
        self.third_user_post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(old_third_user_post, self.third_user_post)

    def test_authorized_upvote_post(self):
        '''
            authorized user can upvote any post
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        first_upvote_response = self.client.put(reverse('post_upvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(first_upvote_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first_upvote_response.json(), serializer.data)

        second_upvote_response = self.client.put(reverse('post_upvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(second_upvote_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(second_upvote_response.json(), serializer.data)

        self.client.put(reverse('post_downvote',
            kwargs={"pk": self.third_user_post.id}))
        third_upvote_response = self.client.put(reverse('post_upvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(third_upvote_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(third_upvote_response.json(), serializer.data)

    def test_authorized_downvote_post(self):
        '''
            authorized user can downvote any post
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        first_upvote_response = self.client.put(reverse('post_downvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(first_upvote_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first_upvote_response.json(), serializer.data)

        second_upvote_response = self.client.put(reverse('post_downvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(second_upvote_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(second_upvote_response.json(), serializer.data)

        self.client.put(reverse('post_upvote',
            kwargs={"pk": self.third_user_post.id}))
        third_upvote_response = self.client.put(reverse('post_downvote',
            kwargs={"pk": self.third_user_post.id}))

        self.third_user_post.refresh_from_db()
        serializer = PostSerializer(self.third_user_post)
        self.assertEqual(third_upvote_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(third_upvote_response.json(), serializer.data)

    def test_unauthorized_upvote_downvote(self):
        '''
            unauthorized user can't upvote or downvote the post
        '''
        upvote_response = self.client.put(reverse('post_upvote',
            kwargs={"pk": self.third_user_post.id}))
        downvote_reponse = self.client.put(reverse('post_downvote',
            kwargs={"pk": self.third_user_post.id}))

        self.assertEqual(upvote_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(downvote_reponse.status_code, status.HTTP_401_UNAUTHORIZED)
