from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from api.exeptions import CustomApiException
from comments.models import Comment, CommentVote
from .serializers import CommentSerializer, CommentCreateSerializer

class CommentsAndCommentVotesTests(APITestCase):
    '''
        Tests for Comments and CommentVotes
    '''

    def setUp(self):
        '''
            set up test database
        '''
