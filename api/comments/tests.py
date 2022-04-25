from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from userprofile.models import UserProfile
from posts.models import Post
from comments.models import Comment, CommentVote
from .serializers import CommentSerializer, CommentCreateSerializer

User = get_user_model()

class CommentsAndCommentVotesTests(APITestCase):
    '''
        Tests for Comments and CommentVotes
    '''

    def setUp(self):
        '''
            set up test database
        '''

        self.first_user = User.objects.create_user(username='my user',
            email='abcdf@mail.ru', password='qwe123')
        self.first_user.save()
        self.first_userprofile = UserProfile.objects.create(user=self.first_user,
            id=self.first_user.id)
        self.first_userprofile.save()

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

        self.first_user_post = Post.objects.create(owner=self.first_userprofile,
            title="First user post", main_text="Qwe rty")
        self.first_user_post.save()

        self.first_user_post_comment = Comment.objects.create(owner=self.first_userprofile,
            post=self.first_user_post, text="XD")
        self.second_user_post_comment = Comment.objects.create(owner=self.second_userprofile,
            post=self.first_user_post, text="LOL")
        self.third_user_post_comment = Comment.objects.create(owner=self.third_userprofile,
            post=self.first_user_post, text="ROFL")

        self.first_user_first_comment_vote = CommentVote.objects.create(owner=self.first_userprofile,
            comment=self.first_user_post_comment, vote_type='up')
        self.first_user_first_comment_vote.save()
        self.second_user_first_comment_vote = CommentVote.objects.create(owner=self.second_userprofile,
            comment=self.first_user_post_comment, vote_type='up')
        self.second_user_first_comment_vote.save()
        self.third_user_first_comment_vote = CommentVote.objects.create(owner=self.third_userprofile,
            comment=self.first_user_post_comment, vote_type='up')
        self.third_user_first_comment_vote.save()

        self.creation_data = {
            "text": 'meme',
            "post_id": self.first_user_post.id
        }

        self.update_data = {
            "text": 'new text'
        }

        self.invalid_data = {
            "text": ''
        }

    def test_authorized_comment_details(self):
        '''
            any authorized user can get comment details
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        first_response = self.client.get(reverse('comment-detail',
            kwargs={"pk": self.first_user_post_comment.id}))
        second_response = self.client.get(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        third_response = self.client.get(reverse('comment-detail',
            kwargs={"pk": self.first_user_post_comment.id}))

        first_serializer = CommentSerializer(self.first_user_post_comment)
        second_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(third_response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_response.json(), first_serializer.data)
        self.assertEqual(second_response.json(), second_serializer.data)
        self.assertEqual(third_response.json(), first_serializer.data)

    def test_unauthorized_comment_details(self):
        '''
            unauthorized user can't get commnet details
        '''
        response = self.client.get(reverse('comment-detail',
            kwargs={"pk": self.first_user_post_comment.id}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_valid_comment_craete(self):
        '''
            authorized user can create new comments for post with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.post(reverse('comment-list'), self.creation_data)

        serializer = CommentCreateSerializer(Comment.objects.get(text=self.creation_data.get('text')))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), serializer.data)

    def test_authorized_invalid_comment_craete(self):
        '''
            authorized user can't create new comments for post with invalid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.post(reverse('comment-list'), self.invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        try:
            Comment.objects.get(text=self.invalid_data.get(''))
        except Comment.DoesNotExist:
            self.assertRaises(Comment.DoesNotExist)

    def test_unauthorized_comment_create(self):
        '''
            unauthorized user can't create new comments for post
        '''
        response = self.client.post(reverse('comment-list'), self.creation_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_owner_valid_comment_update(self):
        '''
            comment owner can update comment with valid data
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.put(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}), self.update_data)

        self.second_user_post_comment.refresh_from_db()
        serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_owner_invalid_comment_update(self):
        '''
            comment owner can't update comment with invalid data
        '''
        old_second_user_post_comment = self.second_user_post_comment

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.put(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}), self.invalid_data)

        self.second_user_post_comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.second_user_post_comment, old_second_user_post_comment)

    def test_postowner_user_comment_update(self):
        '''
            post owner and user can't update comment of another user
        '''
        old_second_user_post_comment = self.second_user_post_comment

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        first_reponse = self.client.put(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}), self.update_data)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        second_reponse = self.client.put(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}), self.update_data)

        self.second_user_post_comment.refresh_from_db()

        self.assertEqual(first_reponse.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(second_reponse.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.second_user_post_comment, old_second_user_post_comment)

    def test_unauthorized_comment_update(self):
        '''
            unauthorized user can't update comment
        '''
        response = self.client.put(reverse('comment-detail',
            kwargs={"pk": self.first_user_post_comment.id}), self.update_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_comment_delete(self):
        '''
            comment owner can delete his comment
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.second_user_token))
        response = self.client.delete(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            Comment.objects.get(text="LOL")
        except Comment.DoesNotExist:
            self.assertRaises(Comment.DoesNotExist)

    def test_postowner_comment_delete(self):
        '''
            post owner can delete comment of another user
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.first_user_token))
        response = self.client.delete(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        try:
            Comment.objects.get(text="LOL")
        except Comment.DoesNotExist:
            self.assertRaises(Comment.DoesNotExist)

    def test_user_comment_delete(self):
        '''
            user can't delete comment of another user
        '''
        old_second_user_post_comment = self.second_user_post_comment

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        response = self.client.delete(reverse('comment-detail',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_second_user_post_comment, self.second_user_post_comment)

    def test_unauthorized_comment_delete(self):
        '''
            unauthorized user can't delete comment
        '''
        response = self.client.delete(reverse('comment-detail',
            kwargs={"pk": self.first_user_post_comment.id}))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_upvote_comment(self):
        '''
            authorized user can upvote any comment
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        first_response = self.client.put(reverse('comment-upvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        first_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first_response.json(), first_serializer.data)
        self.assertEqual(first_response.json().get('upvotes'), 1)
        self.assertEqual(first_response.json().get('downvotes'), 0)

        second_response = self.client.put(reverse('comment-upvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        second_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(second_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(second_response.json(), second_serializer.data)
        self.assertEqual(second_response.json().get('upvotes'), 0)
        self.assertEqual(second_response.json().get('downvotes'), 0)

        self.client.put(reverse('comment-downvote', kwargs={"pk": self.second_user_post_comment.id}))
        third_response = self.client.put(reverse('comment-upvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        third_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(third_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(third_response.json(), third_serializer.data)
        self.assertEqual(third_response.json().get('upvotes'), 1)
        self.assertEqual(third_response.json().get('downvotes'), 0)

    def test_authorized_downvote_comment(self):
        '''
            authorized user can downvote any comment
        '''
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.third_user_token))
        first_response = self.client.put(reverse('comment-downvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        first_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(first_response.json(), first_serializer.data)
        self.assertEqual(first_response.json().get('upvotes'), 0)
        self.assertEqual(first_response.json().get('downvotes'), 1)

        second_response = self.client.put(reverse('comment-downvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        second_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(second_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(second_response.json(), second_serializer.data)
        self.assertEqual(second_response.json().get('upvotes'), 0)
        self.assertEqual(second_response.json().get('downvotes'), 0)

        self.client.put(reverse('comment-upvote', kwargs={"pk": self.second_user_post_comment.id}))
        third_response = self.client.put(reverse('comment-downvote',
            kwargs={"pk": self.second_user_post_comment.id}))

        self.second_user_post_comment.refresh_from_db()
        third_serializer = CommentSerializer(self.second_user_post_comment)

        self.assertEqual(third_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(third_response.json(), third_serializer.data)
        self.assertEqual(third_response.json().get('upvotes'), 0)
        self.assertEqual(third_response.json().get('downvotes'), 1)


    def test_unauthorized_upvote_downvote_comment(self):
        '''
            unauthorized user can't upvote/downvote any comment
        '''
        first_response = self.client.put(reverse('comment-upvote',
            kwargs={"pk": self.first_user_post_comment.id}))
        second_resposne = self.client.put(reverse('comment-downvote',
            kwargs={"pk": self.first_user_post_comment.id}))

        self.assertEqual(first_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(second_resposne.status_code, status.HTTP_401_UNAUTHORIZED)
