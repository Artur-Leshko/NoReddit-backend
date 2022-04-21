from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from api.exeptions import CustomApiException
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
            post=self.first_user_post_comment, vote_type='up')
        self.second_user_first_comment_vote.save()
        self.third_user_first_comment_vote = CommentVote.objects.create(owner=self.third_userprofile,
            post=self.first_user_post_comment, vote_type='up')
        self.third_user_first_comment_vote.save()

        self.first_user_second_comment_vote = CommentVote.objects.create(owner=self.first_userprofile,
            post=self.second_user_post_comment, vote_type='up')
        self.first_user_second_comment_vote.save()
        self.second_user_second_comment_vote = CommentVote.objects.create(owner=self.second_userprofile,
            post=self.second_user_post_comment, vote_type='up')
        self.second_user_second_comment_vote.save()
        self.third_user_second_comment_vote = CommentVote.objects.create(owner=self.third_userprofile,
            post=self.second_user_post_comment, vote_type='down')
        self.third_user_second_comment_vote.save()
